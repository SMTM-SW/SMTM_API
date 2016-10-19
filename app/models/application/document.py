import datetime

from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TIMESTAMP
from sqlalchemy.sql.expression import text

from app import app, db


class DocumentModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'documents'
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
    board_id = db.Column(
        INTEGER(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'boards.id')))
    )
    title = db.Column(
        db.String(250),
        nullable=False
    )
    content = db.Column(
        LONGTEXT,
        nullable=False
    )
    read_count = db.Column(
        INTEGER(unsigned=True),
        default=0
    )
    like_count = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
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

    boards = db.relationship(
        'BoardModel',
        backref='document'
    )
    users = db.relationship(
        'UserModel',
        backref='document',
        lazy='joined'
    )
