from app.models.application.board import BoardModel
from app.models.application.document import DocumentModel
from app.models.application.user import UserModel


def getDocumentBaseQuery():
    return DocumentModel.query. \
        with_entities(DocumentModel.id,
                      DocumentModel.title,
                      DocumentModel.content,
                      DocumentModel.board_id,
                      BoardModel.name.label('board_name'),
                      BoardModel.title.label('board_title'),
                      DocumentModel.read_count,
                      DocumentModel.like_count,
                      DocumentModel.user_id,
                      UserModel.username.label('username'),
                      DocumentModel.created_date). \
        filter(DocumentModel.board_id == BoardModel.id). \
        filter(DocumentModel.user_id == UserModel.id). \
        filter(DocumentModel.status == 'public')


def getDocumentQuery(document_id):
    return getDocumentBaseQuery(). \
        filter(DocumentModel.id == document_id)


def getDocumentListQuery(target_board):
    return getDocumentBaseQuery(). \
        filter(DocumentModel.board_id == target_board.id)
