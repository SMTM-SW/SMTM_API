import datetime

from sqlalchemy.dialects.mysql import TEXT, TIMESTAMP, BIGINT
from sqlalchemy.sql.expression import text

from app import app, db, bcrypt


class UserModel(db.Model):
    __bind_key__ = app.config.get('DEFAULT_DATABASE')
    __tablename__ = 'users'
    __table_args__ = {
        'schema': __bind_key__,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    gender_enums = ('male', 'female')
    type_enums = ('unregistered', 'registered', 'manager', 'withdrawal')

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    password = db.Column(
        TEXT,
        nullable=False
    )
    name = db.Column(
        db.String(80),
        nullable=True
    )
    gender = db.Column(
        db.Enum(*gender_enums),
        default=gender_enums[0],
        server_default=gender_enums[0]
    )
    # TODO: 외부 클라이언트와 중복(unique) 불가 처리 필요.
    nickname = db.Column(
        db.String(80),
        unique=True
    )
    email = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    type = db.Column(
        db.Enum(*type_enums),
        default=type_enums[0],
        server_default=type_enums[0]
    )
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )

    def is_valid_password(self, input_value):
        return bcrypt.check_password_hash(self.password, input_value)

    documents = db.relationship(
        'DocumentModel',
        backref='user'
    )
