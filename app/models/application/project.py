import datetime

from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TIMESTAMP, TINYTEXT
from sqlalchemy.sql.expression import text

from app import app, db


class ProjectModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'projects'
    __table_args__ = {
        'schema': __bind_key__,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    status_enum = ('waiting', 'working', 'done', 'error')
    contact_type_enum = ('none', 'email', 'sms', 'both')

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    description = db.Column(
        TINYTEXT,
        nullable=False
    )
    user_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'users.id'))),
        nullable=False
    )
    target_count = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    status = db.Column(
        db.Enum(*status_enum),
        default=status_enum[0],
        server_default=status_enum[0],
        nullable=False
    )
    contact_type = db.Column(
        db.Enum(*contact_type_enum),
        default=contact_type_enum[0],
        server_default=contact_type_enum[0],
        nullable=False
    )
    valid_customer = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    keyword_num = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    is_activated = db.Column(
        db.Boolean,
        default=True,
        server_default='1',
        nullable=False
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )

    users = db.relationship(
        'UserModel',
        backref='project',
        lazy='joined'
    )
