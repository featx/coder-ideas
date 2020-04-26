from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.project_template import ProjectTemplate


class ProjectTemplateService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    def find_by_project_code(self, project_code):
        session = self._scoped_session()
        return session.query(ProjectTemplate).filter_by(project_code=project_code).all()

    @transactional
    def create(self, project_template: ProjectTemplate):
        session = self._scoped_session()
        if project_template.code is None or project_template.code.strip() == "":
            project_template.code = "PTL{}".format(self.__id_generator.next_base_36())
        last_template = session.query(ProjectTemplate) \
            .filter_by(project_code=project_template.project_code) \
            .order_by(ProjectTemplate.sort.desc()) \
            .first()
        if last_template is None:
            project_template.sort = 1
        else:
            project_template.sort = last_template.sort + 1
        session.add(project_template)
        return project_template
