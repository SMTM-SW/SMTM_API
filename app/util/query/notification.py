from app.models.application.notification import NotificationModel


def getNotificationListQuery(request_user_id):
    return NotificationModel.query. \
        with_entities(NotificationModel.id,
                      NotificationModel.content,
                      NotificationModel.extra_data,
                      NotificationModel.target_id,
                      NotificationModel.status,
                      NotificationModel.created_date). \
        filter_by(user_id=request_user_id). \
        filter_by(status='unread')
