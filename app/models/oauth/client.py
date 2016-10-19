import datetime

from sqlalchemy.dialects.mysql import BIGINT, TEXT, TIMESTAMP
from sqlalchemy.sql.expression import text

from app import app, db


class ClientModel(db.Model):
    __bind_key__ = app.config.get('OAUTH_DATABASE')
    __tablename__ = 'clients'
    __table_args__ = {
        'schema': __bind_key__,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }
    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        autoincrement=True,
        index=True
    )
    name = db.Column(
        db.String(200),
        nullable=False
    )
    description = db.Column(
        TEXT
    )
    logo_url = db.Column(
        db.String(200)
    )
    homepage_url = db.Column(
        db.String(200)
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.datetime.utcnow()
        self.updated_date = datetime.datetime.utcnow()

    @property
    def redirect_uris(self):
        app.logger.debug("credential: {0}".format(self.credential[0]))

        if self.credential:
            return self.credential[0].callback.split(',')
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]
