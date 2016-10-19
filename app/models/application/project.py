import datetime

from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
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

    id = db.Column(
        INTEGER(20, unsigned=True),
        primary_key=True,
        index=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    user_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'users.id'))),
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
