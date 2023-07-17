from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, DATE
import uuid

Base = declarative_base()


class StatsMessage(Base):
    __tablename__ = "statistics"

    customerid = Column(Integer)
    type = Column(String)
    amount = Column(Numeric(10, 3))
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DATE)
