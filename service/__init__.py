def transactional(func):
    def actual_func(self, *args):
        session = self._scoped_session()
        try:
            result = func(self, *args)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
    return actual_func
