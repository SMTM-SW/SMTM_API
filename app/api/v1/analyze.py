from flask import request
from flask_restful import Resource
from yagmail import yagmail

from app import api_root, db, app, oauth_provider
from app.api.api_request import RequestCrawlerAPI
from app.api.exceptions import NotFoundError
from app.models.application.notification import NotificationModel
from app.models.application.project import ProjectModel
from app.models.application.project_keyword import ProjectKeywordModel
from app.models.application.user import UserModel
from app.util.query.target import getProjectTargetQuery


@api_root.resource('/v1/project/<int:project_id>/analyze')
class Analyze(Resource):
    @oauth_provider.require_oauth('profile')
    def get(self, project_id):
        request_user = request.oauth.user
        query = getProjectTargetQuery(project_id)
        targets = query.all()

        if not targets:
            raise NotFoundError

        output = list()
        for target in targets:
            data = dict(zip(target.keys(), target))
            output.append(data)

        request_body = {
            'items': output,
            'project_id': project_id
        }

        try:
            response_data = RequestCrawlerAPI.crawler_init(request_body)
        except:
            return {
                'success': False,
                'messages': [
                    '크롤러 서버에 에러가 발생하였습니다.'
                ]
            }

        if not response_data['success']:
            return {
                'success': False,
                'messages': [
                    '분석에 오류가 발생했습니다!'
                ]
            }

        project = ProjectModel.query.filter_by(id=project_id).one()
        project.status = 'working'

        subject = "Lookalike 앱 분석이 시작되었습니다."
        body = """<div style='background-color:#EEEEEE ;width:540px;background-image:-moz-linear-gradient(top left,#53b2de 0%,#EEEEEE 50%);\
                font-family:'Lucida Grande','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;line-height:18px;color:#555555 '> \
                <div style='width:500px;padding:20px 20px;margin: 0em auto'> <div style='margin: 20px 175px'> \
                <img src='https://s3-ap-northeast-1.amazonaws.com/yourssu-resource/images/logo.png' width='150' height='70' alt='yourssu logo'> </div> \
                <div style='background-color:#fff;border-radius:2px;padding:40px'> <div style='width:50%;min-height:20%;max-width:300px'> </div> \
                <div style='width:50%;min-height:20%;max-width:300px'> </div> <span style='font-size:18px;line-height:18px;color:#000000 ;font-weight:normal'> \
                Lookalike 앱 분석이 시작되었습니다. </span> <br> <br> 현재 분석이 진행중입니다. 분석이 완료되면 이메일이 다시 발송됩니다. <br> <br> <br> \
                <a style='text-align:center;text-decoration:none;font-size:16px;color:white;background-color:#1dccaa ;width:210px;max-width:90%;\
                margin:0px auto 0px auto;padding:14px 7px 14px 7px;display:block;border:0px;border-radius:3px' href='{0}' target='_blank'>Lookalike으로 이동하기</a>\
                <br> <br> 위 버튼으로 이동하지 않는 경우 다음 주소를 브라우저에 입력해주세요. <br> <br> <a href='{0}'>\
                {0}</a> <br> <br> Lookalike을 이용해주셔서 감사합니다. <br> \
                </div> <div style='padding:0px 15px;font-size:11px;line-height:11px;margin-top:22px'> \
                <a href='{0}' target='_blank'>Lookalike</a>의 분석 서비스에 이 메일 주소를 입력하여 본 메일이 전송되었습니다.<br> \
                분석 서비스를 사용하지 않았다면 본 메일을 무시하셔도 좋습니다. 본 메일은 회신용이 아닙니다. </div> \
                <div style='padding:0px 15px;font-size:11px;line-height:11px;margin-top:11px'> Lookalike. \
                서울 특별시 강남구 테헤란로 311(역삼동) 아남타워 빌딩 6층, 7층  </div> </div> </div>""".format(app.config['HOST_CLIENT'])
        body = body.encode('utf-8').decode('utf-8')

        user = UserModel.query.filter_by(id=project.user_id).one()
        yagmail.SMTP(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']).send(to=[user.email], subject=subject,
                                                                                    contents=body)
        new_notification = NotificationModel(
            content='{0}의 분석이 시작되었습니다.'.format(project.title),
            extra_data=['분석이 완료되면 이메일이 발송됩니다!'],
            target_id=project_id,
            user_id=request_user.id,
        )
        db.session.add(new_notification)
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '분석이 성공적으로 시작되었습니다.'
            ]
        }

    def post(self, project_id):
        request_body = request.get_json()

        result = request_body['result']
        for i in result:
            new_keyword = ProjectKeywordModel(
                project_id=project_id,
                ranking=i['ranking'],
                keyword=i['keyword'],
                lookalike_score=i['lookalike_score'],
                found_target=i['found_target'],
                advertise_range=i['advertise_range']
            )
            db.session.add(new_keyword)

        project = ProjectModel.query.filter_by(id=project_id).one()
        project.status = 'done'

        subject = "Lookalike 앱 분석이 완료되었습니다."
        body = """<div style='background-color:#EEEEEE ;width:540px;background-image:-moz-linear-gradient(top left,#53b2de 0%,#EEEEEE 50%);\
                font-family:'Lucida Grande','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;line-height:18px;color:#555555 '> \
                <div style='width:500px;padding:20px 20px;margin: 0em auto'> <div style='margin: 20px 175px'> \
                <img src='https://s3-ap-northeast-1.amazonaws.com/yourssu-resource/images/logo.png' width='150' height='70' alt='yourssu logo'> </div> \
                <div style='background-color:#fff;border-radius:2px;padding:40px'> <div style='width:50%;min-height:20%;max-width:300px'> </div> \
                <div style='width:50%;min-height:20%;max-width:300px'> </div> <span style='font-size:18px;line-height:18px;color:#000000 ;font-weight:normal'> \
                Lookalike 앱 분석이 완료되었습니다. </span> <br> <br> 분석이 완료되었습니다. 홈페이지로 이동해서 분석 결과를 확인하세요. <br> <br> <br> \
                <a style='text-align:center;text-decoration:none;font-size:16px;color:white;background-color:#1dccaa ;width:210px;max-width:90%;\
                margin:0px auto 0px auto;padding:14px 7px 14px 7px;display:block;border:0px;border-radius:3px' href='{0}' target='_blank'>Lookalike으로 이동하기</a>\
                <br> <br> 위 버튼으로 이동하지 않는 경우 다음 주소를 브라우저에 입력해주세요. <br> <br> <a href='{0}'>\
                {0}</a> <br> <br> Lookalike을 이용해주셔서 감사합니다. <br> \
                </div> <div style='padding:0px 15px;font-size:11px;line-height:11px;margin-top:22px'> \
                <a href='{0}' target='_blank'>Lookalike</a>의 분석 서비스에 이 메일 주소를 입력하여 본 메일이 전송되었습니다.<br> \
                분석 서비스를 사용하지 않았다면 본 메일을 무시하셔도 좋습니다. 본 메일은 회신용이 아닙니다. </div> \
                <div style='padding:0px 15px;font-size:11px;line-height:11px;margin-top:11px'> Lookalike. \
                서울 특별시 강남구 테헤란로 311(역삼동) 아남타워 빌딩 6층, 7층  </div> </div> </div>""".format(app.config['HOST_CLIENT'])
        body = body.encode('utf-8').decode('utf-8')

        user = UserModel.query.filter_by(id=project.user_id).one()
        yagmail.SMTP(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']).send(to=[user.email], subject=subject,
                                                                                    contents=body)

        new_notification = NotificationModel(
            content='{0}의 분석이 완료되었습니다.'.format(project.title),
            extra_data=['프로젝트 페이지로 이동해 분석 결과를 확인하세요!'],
            target_id=project_id,
            user_id=project.user_id,
        )
        db.session.add(new_notification)
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '성공적으로 반영되었습니다.'
            ]
        }
