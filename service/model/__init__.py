from datetime import datetime

from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, Integer


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
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    type = Column(Integer(), default=0, nullable=False)
