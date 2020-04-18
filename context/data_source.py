import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

config = yaml.load()

engine = create_engine(
        "mysql+pymysql://root:123456@127.0.0.1:3306/s9day120?charset=utf8mb4",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
SessionFactory = sessionmaker(bind=engine)
session = scoped_session(SessionFactory)
