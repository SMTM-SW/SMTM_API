from flask_restful import Resource, marshal_with

from app import api_root
from app.api.marshals import analyze_result_fields
from app.models.application.project import ProjectModel
from app.models.application.project_demo import ProjectDemoModel
from app.models.application.project_keyword import ProjectKeywordModel


@api_root.resource('/v1/project/<int:project_id>/result')
class Result(Resource):
    # @oauth_provider.require_oauth('profile')
    @marshal_with(analyze_result_fields)
    def get(self, project_id):
        project = ProjectModel.query.filter_by(id=project_id).one()
        keywords = ProjectKeywordModel.query.filter_by(project_id=project_id).all()
        demos = ProjectDemoModel.query.filter_by(project_id=project_id).all()

        keyword_list = list()
        for keyword in keywords:
            data = dict(zip(keyword.keys(), keyword))
            keyword_list.append(data)

        demo_list = list()
        for demo in demos:
            data = dict(zip(demo.keys(), demo))
            demo_list.append(data)

        return {
            'project': project,
            'keyword': keyword_list,
            'demo': demo_list,
        }
