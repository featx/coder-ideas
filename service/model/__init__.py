from datetime import datetime

from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, Integer
from sqlalchemy.orm import Query


class Identified:
    id = Column(BigInteger(), primary_key=True, nullable=False)
    deleted = Column(Boolean(), default=False, nullable=False)

    def is_new(self):
        return self.id is None


class Record(Identified):
    created_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Update(Record):
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Unified(Update):
    code = Column(String(), unique=True, default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    type = Column(Integer(), default=0, nullable=False)


class Page:
    page = 1
    size = 10

    def __init__(self, dict):
        self.__dict__.update(dict)
        if self.page <= 1:
            self.page = 1
        if self.size <= 0:
            self.size = 10

    def offset(self):
        return (self.page - 1) * self.size

    def as_page(self, query: Query):
        if query is None:
            return None
        return query.offset(self.offset()).limit(self.size)