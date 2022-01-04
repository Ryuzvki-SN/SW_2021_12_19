from api import ma
from api.notifications.model import Notification


class NotificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Notification

    id = ma.auto_field()
    request = ma.auto_field()


notification_schema = NotificationSchema(partial=True)
notifications_schema = NotificationSchema(many=True)
