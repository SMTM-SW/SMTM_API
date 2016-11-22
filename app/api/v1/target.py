from flask import request
from flask_restful import Resource, marshal_with

from app import api_root, oauth_provider, db
from app.api.exceptions import NotFoundError
from app.api.marshals import project_target_list_field
from app.api.util import check_str
from app.models.application.notification import NotificationModel
from app.models.application.project import ProjectModel
from app.models.application.project_target import ProjectTargetModel
from app.models.application.target import TargetModel
from app.util.query.target import getProjectTargetQuery


@api_root.resource('/v1/project/<int:project_id>/target')
class Target(Resource):
    @marshal_with(project_target_list_field)
    def get(self, project_id):
        query = getProjectTargetQuery(project_id)
        targets = query.all()

        if not targets:
            raise NotFoundError

        output = list()
        for target in targets:
            data = dict(zip(target.keys(), target))
            output.append(data)

        return {
            'items': output
        }

    @oauth_provider.require_oauth('profile')
    def post(self, project_id):
        request_user = request.oauth.user
        request_body = request.get_json()
        target = request_body['target']

        check_duplicate = ProjectTargetModel.query.filter_by(project_id=project_id).all()
        if check_duplicate:
            for i in check_duplicate:
                i.is_activated = 0
                db.session.commit()

        project = ProjectModel.query.filter_by(id=project_id).one()
        project.target_count = len(target)

        for i in target:
            new_target = TargetModel(
                name=check_str(i, 'name'),
                user_id=check_str(i, 'id'),
                nickname=check_str(i, 'nickname'),
                phone=check_str(i, 'phone'),
                email=check_str(i, 'email'),
                birthday=check_str(i, 'birth'),
                gender=check_str(i, 'gender')
            )

            db.session.add(new_target)
            db.session.flush()

            new_project_target = ProjectTargetModel(
                project_id=project_id,
                target_id=new_target.id
            )
            db.session.add(new_project_target)

        new_notification = NotificationModel(
            content='{0} 에 타겟이 등록됬습니다.'.format(project.title),
            extra_data=['분석 시작 버튼을 눌러주세요!'],
            target_id=project_id,
            user_id=request_user.id,
        )
        db.session.add(new_notification)
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '성공적으로 반영되었습니다.'
            ]
        }
