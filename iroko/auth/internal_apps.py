from flask import Blueprint
from flask_login import login_required
from invenio_oauth2server.views.server import error_handler as oauth_error_handler, authorize as oauth_authorized
from invenio_oauth2server.provider import oauth2
from flask import Blueprint, request, abort, current_app
from invenio_oauth2server.models import Client

blueprint = Blueprint(
    'internal_apps',
    __name__,
)


@blueprint.route('/oauth/internal/authorize', methods=['GET', 'POST'])
@login_required
@oauth_error_handler
@oauth2.authorize_handler
def authorize(*args, **kwargs):
    """View for rendering authorization request."""
    if request.method == 'GET':
        client = Client.query.filter_by(
            client_id=kwargs.get('client_id')
        ).first()

        if not client:
            abort(404)
        internal_apps = current_app.config['INTERNAL_CLIENT_APPS_SECRETS']
        print("***************************")
        print(client.client_secret)
        print(internal_apps)
        print("***************************")
        if client.client_secret in internal_apps:
            return True

    return oauth_authorized(*args, **kwargs)
