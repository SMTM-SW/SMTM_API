from app.models.application.project import ProjectModel
from app.models.application.user import UserModel


def getProjectListQuery(request_user_id):
    return ProjectModel.query. \
        with_entities(ProjectModel.id,
                      ProjectModel.title,
                      ProjectModel.description,
                      ProjectModel.status,
                      ProjectModel.user_id,
                      UserModel.username.label('username'),
                      ProjectModel.created_date). \
        filter_by(user_id=request_user_id). \
        filter_by(is_activated=True). \
        filter(ProjectModel.user_id == UserModel.id)

# def getDocumentListQuery():
#     return DocumentModel.query. \
#         with_entities(DocumentModel.id,
#                       DocumentModel.title,
#                       DocumentModel.content,
#                       DocumentModel.read_count,
#                       DocumentModel.like_count,
#                       DocumentModel.user_id,
#                       UserModel.username.label('username'),
#                       DocumentModel.created_date). \
#         filter(DocumentModel.user_id == UserModel.id)
