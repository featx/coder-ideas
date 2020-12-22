from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.template_rule import TemplateRule


class TemplateRuleService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    @transactional
    def create(self, template_rule: TemplateRule):
        session = self._scoped_session()
        if template_rule.code is None or template_rule.code.strip() == "":
            template_rule.code = "TRL{}".format(self.__id_generator.next_base_36())
        session.add(template_rule)
        return template_rule

    @transactional
    def update(self, update_rule: TemplateRule):
        if update_rule.code is None or update_rule.code.strip() == "":
            return None
        session = self._scoped_session()
        rule = session.query(TemplateRule).filter_by(code=update_rule.code).first()
        if rule is None:
            return None
        rule.override_by(update_rule)
        return rule

    def find_by_code(self, code):
        if code is None or code.strip() == "":
            return None
        session = self._scoped_session()
        return session.query(TemplateRule).filter_by(code=code).first()

    def list_of(self, template_code: str):
        pass

    @transactional
    def find_by_template_code(self, template_code: str):
        session = self._scoped_session()
        return session.query(TemplateRule).filter_by(template_code=template_code) \
            .order_by(TemplateRule.sort).all()
