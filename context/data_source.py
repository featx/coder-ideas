from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def create_session_factory(data_source_param):
    engine = create_engine(
        "mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4".format_map(data_source_param),
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    return sessionmaker(bind=engine)


def create_transaction(session_factory: sessionmaker):
    def transactional(service_func):
        def wrapper(*service_func_args):
            session = scoped_session(session_factory)
            try:
                service_func(*service_func_args)
                session.commit()
            except Exception as e:
                session.rollback()
            session.remove()
        return wrapper
    return transactional
