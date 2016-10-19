import datetime

from sqlalchemy.dialects.mysql import BIGINT, TEXT, TIMESTAMP, DATETIME
from sqlalchemy.sql.expression import text

from app import app, db


class GrantTokenModel(db.Model):
    __bind_key__ = app.config.get('OAUTH_DATABASE')
    __tablename__ = 'grant_tokens'
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
    app_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((__bind_key__, 'clients.id')), ondelete='CASCADE'),
        nullable=False
    )
    application = db.relationship('ClientModel', lazy='joined')
    owner_id = db.Column(
        BIGINT(20, unsigned=True),
        db.ForeignKey('.'.join((app.config.get('DEFAULT_DATABASE'), 'users.id'))),
        nullable=False
    )
    user = db.relationship('UserModel',
                           backref='grant_token',
                           lazy='joined')
    code = db.Column(
        db.String(255),
        nullable=False
    )
    expires_date = db.Column(
        DATETIME,
        nullable=False
    )
    redirect_uri = db.Column(
        db.String(255),
        nullable=False
    )
    scope = db.Column(
        TEXT,
        nullable=False
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []
