import datetime

from sqlalchemy.dialects.mysql import BIGINT, TINYTEXT, TIMESTAMP
from sqlalchemy.sql.expression import text

from app import app, db


class NotificationModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'notifications'
    __table_args__ = {
        'schema': __bind_key__,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    status_enum = ('unread', 'read', 'hidden')

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )
    content = db.Column(
        TINYTEXT,
        nullable=False
    )
    extra_data = db.Column(
        TINYTEXT
    )
    target_id = db.Column(
        BIGINT(20, unsigned=True),
        nullable=False
    )
    user_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'users.id'))),
        nullable=False
    )
    status = db.Column(
        db.Enum(*status_enum),
        default=status_enum[0],
        server_default=status_enum[0],
        nullable=False
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
