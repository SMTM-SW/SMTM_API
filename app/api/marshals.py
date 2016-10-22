from flask_restful import fields

user_check_field = {
    'is_user': fields.String(attribute='is_user'),
    'is_first': fields.String(attribute='is_first')
}


user_field = {
    'username': fields.String(attribute='username'),
    'nickname': fields.String(attribute='nickname'),
    'name': fields.String(attribute='name'),
    'gender': fields.String(attribute='gender'),
    'company': fields.String(attribute='company'),
    'type': fields.String(attribute='type'),
    'email': fields.String(attribute='email'),
    'join': fields.String(attribute='created_date')
}

document_field = {
    "id": fields.Integer(attribute='id'),
    "title": fields.String(attribute='title'),
    "content": fields.String(attribute="content"),
    "read_count": fields.Integer(attribute="read_count"),
    "like_count": fields.Integer(attribute="like_count"),
    "user_id": fields.Integer(attribute="user_id"),
    "username": fields.String(attribute="username"),
    "created_date": fields.String(attribute="created_date")
}

project_field = {
    "id": fields.Integer(attribute='id'),
    "title": fields.String(attribute='title'),
    "description": fields.String(attribute="description"),
    "target_count": fields.Integer(attribute="target_count"),
    # TODO: interest 항목 나중에 추가
    "interest_id": fields.String(attribute="interest_id"),
    "contact_type": fields.String(attribute="contact_type"),
    "status": fields.String(attribute="status"),
    # TODO : user_id는 나중에 모두 뺄 수 있도록
    "user_id": fields.Integer(attribute="user_id"),
    "username": fields.String(attribute="username"),
    "created_date": fields.String(attribute="created_date")
}

project_list_fields = {
    'items': fields.Nested(project_field)
}
