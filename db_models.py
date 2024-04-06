from sqlalchemy import Column, Integer, String, DateTime

from db_session import Base


class PWLog(Base):
    __tablename__ = "PWLog"

    id = Column(String, primary_key=True, index=True)
    time_stamp = Column(DateTime)
    status_type = Column(String)
    message = Column(String)
