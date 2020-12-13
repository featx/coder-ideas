from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.template import Template, TemplatePageCriteria


class TemplateService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    @transactional
    def create(self, template: Template):
        session = self._scoped_session()
        if template.code is None or template.code.strip() == "":
            template.code = "TPL{}".format(self.__id_generator.next_base_36())
        session.add(template)
        return template

    @transactional
    def update(self, update_template: Template):
        if update_template.code is None or update_template.code.strip() == "":
            return None
        session = self._scoped_session()
        template = session.query(Template).filter_by(code=update_template.code).first()
        if template is None:
            return None
        template.override_by(update_template)
        return template

    @transactional
    def delete(self, code: str):
        if code is None or code.strip() == "":
            return None
        session = self._scoped_session()
        template = session.query(Template).filter_by(code=code).first()
        if template is None:
            raise Exception
        template.deleted = True
        return True

    def find_by_code(self, code: str):
        if code is None or code.strip() == "":
            return None
        session = self._scoped_session()
        return session.query(Template).filter_by(code=code).first()

    @transactional
    def find_by_page_criteria(self, template_model: TemplatePageCriteria):
        c = template_model
        session = self._scoped_session()
        query = c.query(session.query(func.count(Template.id)))
        count = query.first()[0]
        if count <= 0:
            return count, []
        return count, c.query(session.query(Template)).all()

    def list_all(self):
        session = self._scoped_session()
        return session.query(Template).all()
