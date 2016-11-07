import arrow
from flask import request
from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy.orm.exc import NoResultFound

from app import api_root, db, oauth_provider
from app.api.exceptions import NotFoundError, UnauthorizedError
from app.api.marshals import document_field, document_list_fields
from app.models.application.board import BoardModel
from app.models.application.document import DocumentModel
from app.util.query.document import getDocumentQuery, getDocumentListQuery, getDocumentBaseQuery


@api_root.resource('/v1/documents/<int:document_id>')
class Document(Resource):
    @marshal_with(document_field)
    def get(self,document_id):
        try:
            result = getDocumentQuery(document_id).one()
        except NoResultFound:
            raise NotFoundError

        document = Document.get_document(document_id)
        document.read_count += 1
        db.session.commit()

        document = dict(zip(result.keys(), result))
        return document

    @oauth_provider.require_oauth('profile')
    def put(self,document_id):
        request_user = request.oauth.user
        request_body = request.get_json()

        document = Document.get_document(document_id)

        if document.user.id != request_user.id:
            raise UnauthorizedError

        document.title = request_body['title']
        document.content = request_body['content']

        db.session.commit()

        return {
            'success': True,
            'messages': [
                '글이 성공적으로 수정되었습니다.'
            ]
        }

    @oauth_provider.require_oauth('profile')
    def delete(self, document_id):
        document = Document.get_document(document_id)

        document.status = 'hidden'
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '글이 성공적으로 삭제되었습니다.'
            ]
        }

    @staticmethod
    def get_document(document_id):
        try:
            document = DocumentModel.query. \
                filter(DocumentModel.id == document_id). \
                filter(DocumentModel.status == 'public'). \
                one()
        except NoResultFound:
            raise NotFoundError

        return document


@api_root.resource('/v1/boards')
class DocumentRecent(Resource):
    @marshal_with(document_list_fields)
    def get(self):
        param_parser = reqparse.RequestParser()
        param_parser.add_argument('maxResult', type=int, default=10)
        param_parser.add_argument('resultOffset', type=int, default=0)
        args = param_parser.parse_args()

        query = getDocumentBaseQuery()
        result = query. \
            order_by(DocumentModel.id.desc()). \
            offset(args.resultOffset). \
            limit(args.maxResult). \
            all()

        output = list()
        for d in result:
            data = dict(zip(d.keys(), d))
            output.append(data)

        return {
            'items': output
        }


@api_root.resource('/v1/boards/<string:board_name>')
class DocumentList(Resource):
    @marshal_with(document_list_fields)
    def get(self, board_name):

        target_board = DocumentList.get_target_board(board_name)

        param_parser = reqparse.RequestParser()
        param_parser.add_argument('maxResult', type=int, default=10)
        param_parser.add_argument('resultOffset', type=int, default=0)
        args = param_parser.parse_args()

        query = getDocumentListQuery(target_board)
        result = query. \
            order_by(DocumentModel.id.desc()). \
            offset(args.resultOffset). \
            limit(args.maxResult). \
            all()

        output = list()
        for d in result:
            data = dict(zip(d.keys(), d))
            output.append(data)

        return {
            'items': output
        }

    @oauth_provider.require_oauth('profile')
    def post(self,board_name):

        target_board = DocumentList.get_target_board(board_name)

        request_user = request.oauth.user
        request_body = request.get_json()

        new_document = DocumentModel(
            board_id=target_board.id,
            user_id=request_user.id,
            title=request_body['title'],
            content=request_body['content'],
            created_date=arrow.utcnow().datetime
        )

        db.session.add(new_document)
        db.session.commit()

        return {
            'success': True,
            'messages': [
                '글이 정상적으로 작성되었습니다.'
            ]
        }


    @staticmethod
    def get_target_board(board_name):
        try:
            return BoardModel.query. \
                with_entities(BoardModel.id). \
                filter_by(name=board_name). \
                one()

        except NoResultFound:
            raise NotFoundError
