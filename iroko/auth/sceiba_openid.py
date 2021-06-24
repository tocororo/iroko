#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from datetime import datetime, timedelta

from flask import Blueprint, current_app, flash, g, redirect, session, url_for
from flask_babelex import gettext as _
from flask_login import current_user
from flask_principal import (
    AnonymousIdentity, RoleNeed, UserNeed,
    identity_changed, identity_loaded,
    )
from invenio_db import db
from invenio_oauthclient.errors import OAuthResponseError
from invenio_oauthclient.handlers.rest import response_handler
from invenio_oauthclient.models import RemoteAccount
from invenio_oauthclient.proxies import current_oauthclient
from invenio_oauthclient.utils import (
    oauth_link_external_id,
    oauth_unlink_external_id,
    )
from jwt import decode


class OAuthSCEIBARejectedAccountError(OAuthResponseError):
    """Define exception for not allowed sceiba accounts."""


OAUTHCLIENT_SCEIBA_OPENID_REFRESH_TIMEDELTA = timedelta(minutes=-5)
"""Default interval for refreshing SCEIBA extra data (e.g. groups).

False value disabled the refresh.
"""

OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY = "identity.sceiba_openid_provides"
"""Name of session key where SCEIBA roles are stored."""

OAUTHCLIENT_SCEIBA_OPENID_ALLOWED_ROLES = ["sceiba_user"]
"""SCEIBA OAuth application role values that are allowed to be used."""

BASE_APP = dict(
    title="SCEIBA",
    description="Connecting to sceiba.cu",
    icon="",
    logout_url="https://personas.sceiba.cu/auth/realms/sceiba/protocol/"
               "openid-connect/logout",
    params=dict(
        base_url="https://personas.sceiba.cu/auth/realms/sceiba",
        request_token_url=None,
        access_token_url="https://personas.sceiba.cu/auth/realms/sceiba/protocol/"
                         "openid-connect/token",
        access_token_method="POST",
        authorize_url="https://personas.sceiba.cu/auth/realms/sceiba/protocol/"
                      "openid-connect/auth",
        app_key="SCEIBA_APP_OPENID_CREDENTIALS",
        content_type="application/json",
        ),
    )

REMOTE_APP = dict(BASE_APP)
REMOTE_APP.update(
    dict(
        authorized_handler="invenio_oauthclient.handlers"
                           ":authorized_signup_handler",
        disconnect_handler="iroko.auth.sceiba_openid"
                           ":disconnect_handler",
        signup_handler=dict(
            info="iroko.auth.sceiba_openid:account_info",
            setup="iroko.auth.sceiba_openid:account_setup",
            view="invenio_oauthclient.handlers:signup_handler",
            ),
        )
    )
"""SCEIBA Openid Remote Application."""

REMOTE_REST_APP = dict(BASE_APP)
REMOTE_REST_APP.update(
    dict(
        authorized_handler="invenio_oauthclient.handlers.rest"
                           ":authorized_signup_handler",
        disconnect_handler="iroko.auth.sceiba_openid"
                           ":disconnect_rest_handler",
        signup_handler=dict(
            info="iroko.auth.sceiba_openid:account_info_rest",
            setup="iroko.auth.sceiba_openid:account_setup",
            view="invenio_oauthclient.handlers.rest:signup_handler",
            ),
        response_handler=(
            "invenio_oauthclient.handlers.rest:default_remote_response_handler"
        ),
        authorized_redirect_url="/",
        disconnect_redirect_url="/",
        signup_redirect_url="/",
        error_redirect_url="/",
        )
    )
"""SCEIBA Openid Remote REST Application."""

OAUTHCLIENT_SCEIBA_OPENID_USERINFO_URL = (
    "https://personas.sceiba.cu/auth/realms/sceiba/protocol/openid-connect/userinfo"
)

OAUTHCLIENT_SCEIBA_OPENID_JWT_TOKEN_DECODE_PARAMS = dict(
    options=dict(
        verify_signature=False,
        verify_aud=False,
        ),
    algorithms=["HS256", "RS256"]
    )

sceiba_oauth_blueprint = Blueprint("sceiba_openid_oauth", __name__)


def find_remote_by_client_id(client_id):
    """Return a remote application based with given client ID."""
    for remote in current_oauthclient.oauth.remote_apps.values():
        if remote.name == "sceiba_openid" and remote.consumer_key == client_id:
            return remote


def fetch_extra_data(resource):
    """Return a dict with extra data retrieved from SCEIBA OAuth."""
    person_id = resource.get("sceiba_person_id")
    return dict(person_id=person_id)


def account_roles_and_extra_data(account, resource, refresh_timedelta=None):
    """Fetch account roles and extra data from resource if necessary."""
    updated = datetime.utcnow()
    modified_since = updated
    if refresh_timedelta is not None:
        modified_since += refresh_timedelta
    modified_since = modified_since.isoformat()
    last_update = account.extra_data.get("updated", modified_since)

    if last_update > modified_since:
        return account.extra_data.get("roles", [])

    # resource["sceiba_roles"]
    roles = {}
    extra_data = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_EXTRA_DATA_SERIALIZER", fetch_extra_data
        )(resource)

    account.extra_data.update(
        roles=roles, updated=updated.isoformat(), **extra_data
        )
    return roles


def extend_identity(identity, roles):
    """Extend identity with roles based on SCEIBA groups."""
    provides = set(
        [UserNeed(current_user.email)] + [RoleNeed(name) for name in roles]
        )
    identity.provides |= provides
    key = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY",
        OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY,
        )
    session[key] = provides


def disconnect_identity(identity):
    """Disconnect identity from SCEIBA groups."""
    session.pop("sceiba_resource", None)
    key = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY",
        OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY,
        )
    provides = session.pop(key, set())
    identity.provides -= provides


def get_dict_from_response(response):
    """Prepare new mapping with 'Value's grouped by 'Type'."""
    result = {}
    if getattr(response, "_resp") and response._resp.code > 400:
        return result

    for key, value in response.data.items():
        result.setdefault(key, value)
    return result


def get_resource(remote, token_response=None):
    """Query SCEIBA Resources to get user info and roles."""
    cached_resource = session.pop("sceiba_resource", None)
    if cached_resource:
        return cached_resource

    url = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_USERINFO_URL",
        OAUTHCLIENT_SCEIBA_OPENID_USERINFO_URL,
        )
    response = remote.get(url)
    dict_response = get_dict_from_response(response)
    if token_response:
        decoding_params = current_app.config.get(
            "OAUTHCLIENT_SCEIBA_OPENID_JWT_TOKEN_DECODE_PARAMS",
            OAUTHCLIENT_SCEIBA_OPENID_JWT_TOKEN_DECODE_PARAMS,
            )
        token_data = decode(token_response["access_token"], **decoding_params)
        dict_response.update(token_data)
    session["sceiba_resource"] = dict_response
    return dict_response


def _account_info(remote, resp):
    """Retrieve remote account information used to find local user."""
    resource = get_resource(remote, resp)

    print('###########################################3 @########################3')
    print(remote)
    print('###########################################3 @########################3')
    print(resp)
    print('###########################################3 @########################3')
    print(resource)

    valid_roles = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_ALLOWED_ROLES",
        OAUTHCLIENT_SCEIBA_OPENID_ALLOWED_ROLES,
        )
    # sceiba_roles = resource.get("sceiba_roles")
    # if sceiba_roles is None or not set(sceiba_roles).issubset(valid_roles):
    #     raise OAuthSCEIBARejectedAccountError(
    #         "User roles {0} are not one of {1}".format(
    #             sceiba_roles, valid_roles
    #         ),
    #         remote,
    #         resp,
    #     )

    email = resource["email"]
    person_id = resource.get("sceiba_person_id")
    external_id = resource["sub"]
    nice = resource["preferred_username"]
    name = resource["name"]

    return dict(
        user=dict(
            email=email.lower(), profile=dict(username=nice, full_name=name)
            ),
        external_id=external_id,
        external_method="sceiba_openid",
        active=True,
        )


def account_info(remote, resp):
    """Retrieve remote account information used to find local user."""
    try:
        return _account_info(remote, resp)
    except OAuthSCEIBARejectedAccountError as e:
        current_app.logger.warning(e.message, exc_info=True)
        flash(_("SCEIBA account not allowed."), category="danger")
        return redirect("/")


def account_info_rest(remote, resp):
    """Retrieve remote account information used to find local user."""
    try:
        return _account_info(remote, resp)
    except OAuthSCEIBARejectedAccountError as e:
        current_app.logger.warning(e.message, exc_info=True)
        remote_app_config = current_app.config["OAUTHCLIENT_REST_REMOTE_APPS"][
            remote.name
        ]
        return response_handler(
            remote,
            remote_app_config["error_redirect_url"],
            payload=dict(message="SCEIBA account not allowed.", code=400),
            )


def _disconnect(remote, *args, **kwargs):
    """Handle unlinking of remote account."""
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()

    account = RemoteAccount.get(
        user_id=current_user.get_id(), client_id=remote.consumer_key
        )
    external_id = account.extra_data.get("external_id")

    if external_id:
        oauth_unlink_external_id(dict(id=external_id, method="sceiba_openid"))
    if account:
        with db.session.begin_nested():
            account.delete()

    disconnect_identity(g.identity)


def disconnect_handler(remote, *args, **kwargs):
    """Handle unlinking of remote account."""
    _disconnect(remote, *args, **kwargs)
    return redirect(url_for("invenio_oauthclient_settings.index"))


def disconnect_rest_handler(remote, *args, **kwargs):
    """Handle unlinking of remote account."""
    _disconnect(remote, *args, **kwargs)
    redirect_url = current_app.config["OAUTHCLIENT_REST_REMOTE_APPS"][
        remote.name
    ]["disconnect_redirect_url"]
    return response_handler(remote, redirect_url)


def account_setup(remote, token, resp):
    """Perform additional setup after user have been logged in."""
    resource = get_resource(remote, resp)

    with db.session.begin_nested():
        person_id = resource.get("sceiba_person_id")
        external_id = resource.get("sceiba_upn")

        # Set SCEIBA person ID in extra_data.
        token.remote_account.extra_data = {"external_id": external_id}
        roles = account_roles_and_extra_data(token.remote_account, resource)
        assert not isinstance(g.identity, AnonymousIdentity)
        extend_identity(g.identity, roles)

        user = token.remote_account.user
        print(
            '###################account_setup########################3 @########################3'
            )
        print(user)
        # Create user <-> external id link.
        oauth_link_external_id(
            user, dict(id=external_id, method="sceiba_openid")
            )


@identity_changed.connect
def on_identity_changed(sender, identity):
    """Store roles in session whenever identity changes.

    :param identity: The user identity where information are stored.
    """
    if isinstance(identity, AnonymousIdentity):
        disconnect_identity(identity)
        return

    logged_in_via_token = hasattr(current_user, 'login_via_oauth2') \
                          and getattr(current_user, 'login_via_oauth2')

    client_id = current_app.config["SCEIBA_APP_OPENID_CREDENTIALS"][
        "consumer_key"
    ]
    remote_account = RemoteAccount.get(
        user_id=current_user.get_id(), client_id=client_id
        )
    roles = []

    if remote_account and not logged_in_via_token:
        refresh = current_app.config.get(
            "OAUTHCLIENT_SCEIBA_OPENID_REFRESH_TIMEDELTA",
            OAUTHCLIENT_SCEIBA_OPENID_REFRESH_TIMEDELTA,
            )
        if refresh:
            remote = find_remote_by_client_id(client_id)
            resource = get_resource(remote)
            roles.extend(
                account_roles_and_extra_data(
                    remote_account, resource, refresh_timedelta=refresh
                    )
                )
        else:
            roles.extend(remote_account.extra_data["roles"])
    elif remote_account and logged_in_via_token:
        roles.extend(remote_account.extra_data["roles"])

    extend_identity(identity, roles)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """Store roles in session whenever identity is loaded."""
    key = current_app.config.get(
        "OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY",
        OAUTHCLIENT_SCEIBA_OPENID_SESSION_KEY,
        )
    identity.provides.update(session.get(key, []))
