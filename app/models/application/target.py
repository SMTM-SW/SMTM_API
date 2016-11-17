import datetime

from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYTEXT
from sqlalchemy.sql.expression import text

from app import app, db


class TargetModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'targets'
    __table_args__ = {
        'schema': __bind_key__,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )
    name = db.Column(
        TINYTEXT
    )
    user_id = db.Column(
        TINYTEXT
    )
    nickname = db.Column(
        TINYTEXT
    )
    phone = db.Column(
        TINYTEXT
    )
    email = db.Column(
        TINYTEXT
    )
    birthday = db.Column(
        TINYTEXT
    )
    gender = db.Column(
        TINYTEXT
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
