from flask import request
from flask_restful import Resource, marshal_with
from sqlalchemy.orm.exc import NoResultFound

from app import api_root, db, oauth_provider
from app.api.exceptions import NotFoundError, UnauthorizedError, ConflictError
from app.api.marshals import notification_field, notification_list_fields
from app.models.application.notification import NotificationModel
from app.util.query.notification import getNotificationListQuery


@api_root.resource('/v1/notifications')
class NotificationList(Resource):
    @oauth_provider.require_oauth('profile')
    @marshal_with(notification_list_fields)
    def get(self):
        request_user = request.oauth.user

        notification_query = getNotificationListQuery(request_user.id)
        notifications = notification_query. \
            order_by(NotificationModel.id.desc()). \
            all()

        output = list()
        for notification in notifications:
            data = dict(zip(notification.keys(), notification))
            output.append(data)

        return {
            'items': output,
        }


@api_root.resource('/v1/notifications/<int:notification_id>')
class Notification(Resource):
    @oauth_provider.require_oauth('profile')
    @marshal_with(notification_field, envelope='item')
    def get(self, notification_id):
        request_user = request.oauth.user

        try:
            notification = NotificationModel.query.filter_by(id=notification_id).one()

        except NoResultFound:
            raise NotFoundError

        if request_user.id == notification.object_id:
            if notification.status == 'hidden':
                raise ConflictError

            notification.status = 'read'
            db.session.commit()

            return notification

        else:
            raise UnauthorizedError
