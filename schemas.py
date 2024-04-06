from pydantic import BaseModel
from typing import List


class PWLogData(BaseModel):
    id: str
    time_stamp: str
    status_type: str
    message: str


class PWLogList(List[PWLogData]):
    pass
