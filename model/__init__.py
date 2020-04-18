from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class Identified(declarative_base()):
    id = Column(BigInteger(), primary_key=True, nullable=False)
    deleted = Column(Boolean(), default=False, nullable=False)

    def is_new(self):
        return self.id is None


class Record(Identified):
    createdAt = Column(DateTime(), default="current_timestamp", nullable=False)


class Update(Record):
    updatedAt = Column(DateTime(), default="current_timestamp", onupdate="current_timestamp", nullable=False)


class Unified(Update):
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    type = Column(Integer(), default="0", nullable=False)
