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
    'type': fields.String(attribute='type'),
    'email': fields.String(attribute='email')
}

document_field = {
    "id": fields.String(attribute='id'),
    "title": fields.String(attribute='title'),
    "content": fields.String(attribute="content"),
    "read_count": fields.String(attribute="read_count"),
    "like_count": fields.String(attribute="like_count"),
    "user_id": fields.String(attribute="user_id"),
    "username": fields.String(attribute="username"),
    "created_date": fields.String(attribute="created_date")
}

project_field = {
    "id": fields.String(attribute='id'),
    "title": fields.String(attribute='title'),
    "description": fields.String(attribute="description"),
    "status": fields.String(attribute="status"),
    # TODO : user_id는 나중에 모두 뺄 수 있도록
    "user_id": fields.String(attribute="user_id"),
    "username": fields.String(attribute="username"),
    "created_date": fields.String(attribute="created_date")
}

project_list_fields = {
    'items': fields.Nested(project_field)
}
