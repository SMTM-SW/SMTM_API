import datetime

from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, JSON
from sqlalchemy.sql.expression import text

from app import app, db


class ProjectDemoModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'project_demo'
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
    keyword = db.Column(
        db.String(80),
        nullable=False
    )
    keyword_data = db.Column(
        JSON,
        nullable=False
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
