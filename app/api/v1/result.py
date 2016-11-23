from flask import request
from flask_restful import Resource, marshal_with

from app import api_root, oauth_provider
from app.api.marshals import analyze_result_fields
from app.models.application.project_demo import ProjectDemoModel
from app.models.application.project_keyword import ProjectKeywordModel
from app.util.query.project import getProjectQuery


@api_root.resource('/v1/project/<int:project_id>/result')
class Result(Resource):
    @oauth_provider.require_oauth('profile')
    @marshal_with(analyze_result_fields)
    def get(self, project_id):
        request_user = request.oauth.user
        result = getProjectQuery(request_user.id, project_id).one()
        project = dict(zip(result.keys(), result))

        keywords = ProjectKeywordModel.query.filter_by(project_id=project_id).all()
        demos = ProjectDemoModel.query.filter_by(project_id=project_id).all()

        return {
            'project': project,
            'keyword': keywords,
            'demo': demos,
        }
