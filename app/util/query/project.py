from app.models.application.project import ProjectModel
from app.models.application.user import UserModel


def getProjectListQuery(request_user_id):
    return ProjectModel.query. \
        with_entities(ProjectModel.id,
                      ProjectModel.title,
                      ProjectModel.description,
                      ProjectModel.target_count,
                      ProjectModel.contact_type,
                      ProjectModel.status,
                      ProjectModel.user_id,
                      UserModel.username.label('username'),
                      ProjectModel.created_date). \
        filter_by(user_id=request_user_id). \
        filter_by(is_activated=True). \
        filter(ProjectModel.user_id == UserModel.id)


def getProjectQuery(request_user_id, project_id):
    return getProjectListQuery(request_user_id).filter_by(id=project_id)


def modProjectQuery(request_user_id, project_id):
    return ProjectModel.query. \
        filter_by(user_id=request_user_id). \
        filter_by(id=project_id)
