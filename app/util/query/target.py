from app.models.application.project_target import ProjectTargetModel
from app.models.application.target import TargetModel


def getProjectTargetQuery(project_id):
    return ProjectTargetModel.query. \
        with_entities(ProjectTargetModel.project_id,
                      ProjectTargetModel.target_id,
                      TargetModel.name,
                      TargetModel.user_id,
                      TargetModel.nickname,
                      TargetModel.phone,
                      TargetModel.email,
                      TargetModel.birthday,
                      TargetModel.gender). \
        filter_by(project_id=project_id). \
        filter_by(is_activated=True). \
        filter(ProjectTargetModel.target_id == TargetModel.id)
