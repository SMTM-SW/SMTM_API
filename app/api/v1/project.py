from flask import request
from flask_restful import Resource, marshal_with
from sqlalchemy.orm.exc import NoResultFound

from app import api_root, db, oauth_provider
from app.api.exceptions import NotFoundError
from app.api.marshals import project_list_fields, project_field
from app.models.application.project import ProjectModel
from app.util.query.project import getProjectListQuery, getProjectQuery, modProjectQuery


@api_root.resource('/v1/project')
class Project_manage(Resource):
    @oauth_provider.require_oauth('profile')
    @marshal_with(project_list_fields)
    def get(self):
        request_user = request.oauth.user

        projects = getProjectListQuery(request_user_id=request_user.id).all()

        output = list()
        for project in projects:
            data = dict(zip(project.keys(), project))
            output.append(data)

        return {
            'items': output
        }

    @oauth_provider.require_oauth('profile')
    def post(self):
        request_user = request.oauth.user
        request_body = request.get_json()

        new_project = ProjectModel(
            title=request_body['title'],
            description=request_body['description'],
            user_id=request_user.id
        )

        db.session.add(new_project)
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '성공적으로 반영되었습니다.'
            ]
        }


@api_root.resource('/v1/project/<int:project_id>')
class Project(Resource):
    @oauth_provider.require_oauth('profile')
    @marshal_with(project_field)
    def get(self, project_id):
        request_user = request.oauth.user

        try:
            result = getProjectQuery(request_user.id, project_id).one()

        except NoResultFound:
            raise NotFoundError

        project = dict(zip(result.keys(), result))
        return project

    @oauth_provider.require_oauth('profile')
    def put(self, project_id):
        request_user = request.oauth.user
        request_body = request.get_json()

        try:
            result = modProjectQuery(request_user.id, project_id).one()

        except NoResultFound:
            raise NotFoundError

        result.title = request_body['title']
        result.description = request_body['description']

        db.session.commit()

        return {
            'success': True,
            'messages': [
                '성공적으로 반영되었습니다.'
            ]
        }

    @oauth_provider.require_oauth('profile')
    def delete(self, project_id):
        request_user = request.oauth.user

        try:
            result = modProjectQuery(request_user.id, project_id).one()

        except NoResultFound:
            raise NotFoundError

        result.is_activated = False

        db.session.commit()

        return {
            'success': True,
            'messages': [
                '성공적으로 반영되었습니다.'
            ]
        }
