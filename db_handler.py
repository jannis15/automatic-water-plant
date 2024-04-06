from sqlalchemy.orm import Session
from sqlalchemy import desc
from db_models import PWLog
from schemas import PWLogData, PWLogList
from datetime import datetime
from db_session import SessionLocal
import uuid


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_unique_uuid(db: Session, table):
    def generate_uuid() -> str:
        # Generate a random UUID
        random_uuid = uuid.uuid4()
        return str(random_uuid).replace("-", "")

    def uuid_not_in_db(uuid_str: str, db: Session, query_table) -> bool:
        # Check if UUID already exists in the database
        return not db.query(query_table).filter_by(id=uuid_str).first()

    while True:
        # Generate a random UUID
        tmp_uuid = generate_uuid()

        # Check if UUID already exists in the database
        if uuid_not_in_db(tmp_uuid, db, table):
            return tmp_uuid


def datetime_to_utc_string(date_time: datetime) -> str:
    date_str = str(date_time)
    return date_str + '+00:00'


class DBHandler:
    def get_logging_list(self, db: Session) -> PWLogList:
        db_query = db.query(PWLog).order_by(desc(PWLog.time_stamp)).limit(100).all()
        result_list = PWLogList()
        for db_logging_data in db_query:
            result_list.append(PWLogData(
                id=db_logging_data.id,
                time_stamp=datetime_to_utc_string(db_logging_data.time_stamp),
                status_type=db_logging_data.status_type,
                message=db_logging_data.message,
            ))
        return result_list

    def add_log(self, log_data: PWLogData, db: Session):
        db.add(PWLog(
            id=get_unique_uuid(db, PWLog),
            time_stamp=datetime.strptime(log_data.time_stamp, '%Y-%m-%d %H:%M:%S.%f %Z'),
            status_type=log_data.status_type,
            message=log_data.message,
        ))
        db.commit()
