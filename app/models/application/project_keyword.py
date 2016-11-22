import datetime

from sqlalchemy import INTEGER
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from sqlalchemy.sql.expression import text

from app import app, db


class ProjectKeywordModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'project_keyword'
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
    project_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'projects.id'))),
        nullable=False
    )
    ranking = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    keyword = db.Column(
        db.String(80),
        nullable=False
    )
    lookalike_score = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    found_target = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    advertise_range = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        server_default='0'
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
