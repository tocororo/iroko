#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from typing import Dict

from invenio_access.models import ActionUsers
from invenio_accounts.models import User
from invenio_db import db

from iroko.notifications.marshmallow import notification_schema
from iroko.notifications.models import Notification


class Notifications:
    '''Manage Notifications'''

    @classmethod
    def get_notification(cls, id) -> Dict[str, Notification]:
        notif = Notification.query.filter_by(id=id).first()
        if notif:
            return 'ok', notif
        else:
            msg = 'Notification not exist id={0}'.format(id)
            return msg, None

    @classmethod
    def get_notification_receiver(cls, id) -> Dict[str, list]:
        # print('id= ', id)
        notif = Notification.query.filter_by(receiver_id=id).all()
        # print('result= ', notif)
        if notif:
            return 'ok', notif
        else:
            msg = 'Notification not exist id={0}'.format(id)
            return msg, None

    @classmethod
    def edit_notification(cls, id, data) -> Dict[str, Notification]:

        msg, notif = cls.get_notification(id)
        if notif:
            valid_data = notification_schema.load(data)
            if valid_data:
                notif.classification = valid_data['classification']
                notif.description = valid_data['description']
                notif.emiter = valid_data['emiter']
                notif.data = valid_data['data']

                if not notif.receiver_id == valid_data['receiver_id']:
                    # deny al que estaba notif.receiver_id
                    cls.deny_notification_viewed_permission(notif.receiver_id, notif.id)
                    # grant al nuevo valid_data['receiver_id']
                    cls.grant_notification_viewed_permission(valid_data['receiver_id'], notif.id)
                notif.receiver_id = valid_data['receiver_id']
                db.session.commit()
                msg = 'New Notification UPDATED classification={0}'.format(notif.classification)
            else:
                msg = 'errors'
                notif = None
        return msg, notif

    @classmethod
    def viewed_notification(cls, id) -> Dict[str, Notification]:

        msg, notif = cls.get_notification(id)
        if notif:
            notif.viewed = True
            db.session.commit()
            msg = 'New Notification VIEWED classification={0}'.format(notif.classification)
        return msg, notif

    @classmethod
    def new_notification(cls, data) -> Dict[str, Notification]:

        notif_data = notification_schema.load(data)
        if notif_data:
            notif = Notification()
            notif.classification = notif_data['classification']
            notif.description = notif_data['description']
            notif.receiver_id = notif_data['receiver_id']
            notif.emiter = notif_data['emiter']
            notif.data = notif_data['data']
            db.session.add(notif)

            db.session.flush()
            cls.grant_notification_viewed_permission(notif.receiver_id, notif.id)
            db.session.commit()

            msg = 'New Notification CREATED classification={0}'.format(notif.classification)
        else:
            msg = 'Invalid data'
            notif = None
        return msg, notif

    # @classmethod
    # def grant_notification_editor_permission(cls, user_id, notification_id) -> Dict[str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         notification = Notification.query.filter_by(id=notification_id).first()
    #         user = User.query.filter_by(id=user_id)
    #         if not notification:
    #             msg = 'Notification not found'
    #         elif not user:
    #             msg = 'User not found'
    #         else:
    #             db.session.add(ActionUsers.allow(ObjectNotificationEditor(notification.id),
    #             user=user))
    #             if not notification.data:
    #                 notification.data = {'editor':[user.id]}
    #             else:
    #                 notification.data['editor'].append(user.id)

    #             db.session.commit()
    #             msg = 'Editor Permission granted over {0}'.format(notification.name)
    #             done = True

    #     except Exception as e:
    #         msg = str(e)
    #         # print(str(e))

    #     return msg, done

    @classmethod
    def deny_notification_viewed_permission(user_id, notification_id) -> Dict[str, bool]:
        done = False
        msg = ''
        try:
            notification = Notification.query.filter_by(id=notification_id).first()
            user = User.query.filter_by(id=user_id)
            if not notification:
                msg = 'Notification not found'
            elif not user:
                msg = 'User not found'
            else:
                db.session.add(
                    ActionUsers.deny(ObjectNotificationEditor(notification.id), user=user)
                    )

                db.session.commit()
                msg = 'Mark as viewed Permission granted '
                done = True

        except Exception as e:
            # print(str(e))
            msg = str(e)

        return msg, done

    # @classmethod
    # def check_user_notification_editor_permission(user_id, notification_id)-> Dict[str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         notification = Notification.query.filter_by(id=notification_id).first()
    #         user = User.query.filter_by(id=user_id)
    #         user_identity = get_identity(user)
    #         permission = Permission(ObjectNotificationEditor(notification.id))
    #         done = permission.allows(user_identity)
    #     except Exception as e:
    #         msg = str(e)
    #         # print(str(e))

    #     return msg, done

    @classmethod
    def grant_notification_viewed_permission(cls, user_id, notification_id, is_flush=True) -> Dict[
        str, bool]:
        done = False
        msg = ''
        try:
            user = User.query.filter_by(id=user_id)
            if not user:
                msg = 'User not found'
            else:
                db.session.add(
                    ActionUsers.allow(ObjectNotificationEditor(notification_id), user=user)
                    )
                if is_flush:
                    db.session.flush()
                else:
                    db.session.commit()
                msg = 'Notification marking viewed Permission granted '
                done = True

        except Exception as e:
            msg = str(e)
            # print(str(e))

        return msg, done
