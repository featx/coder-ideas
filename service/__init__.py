from context.exception import BusinessError


def transactional(func):
    def actual_func(self, *args):
        session = self._scoped_session()
        try:
            result = func(self, *args)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise BusinessError.SYSTEM_ERROR.with_info(e.args)
    return actual_func
