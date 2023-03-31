import json
from datetime import datetime
from typing import Optional

import structlog

from astraeus_common.decorator.logit import logit
from astraeus_common.error.body_not_found import BodyNotFound
from astraeus_common.io.database import Database
from astraeus_common.models.body import Body


class BodyService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_body_by_key(self, key: dict) -> Optional[Body]:
        raw_data = self._io_db.exec_db_read(Body.BODY_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return Body(raw_data[0])
        else:
            self._log.debug(f'No {Body.__name__} found')
            return None

    @logit
    def read_body_by_system_key(self, system_key: dict) -> Body:
        raw_data = self._io_db.exec_db_read(Body.BODY_SELECT_BY_SYSTEM_KEY, system_key)
        if len(raw_data) == 1:
            return Body(raw_data[0])
        else:
            raise BodyNotFound()

    @logit
    def create_body(self, body_created: Body) -> None:
        body_created.update_time = datetime.now()
        self._io_db.exec_db_write(Body.BODY_INSERT, body_created.to_dict_for_db())

    @logit
    def update_body_by_key(self, body_created: Body) -> None:
        body_created.update_time = datetime.now()
        self._io_db.exec_db_write(Body.BODY_UPDATE_BY_KEY, body_created.to_dict_for_db())

    @logit
    def delete_body_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(Body.BODY_DELETE_BY_KEY, {'key': json.dumps(key)})
