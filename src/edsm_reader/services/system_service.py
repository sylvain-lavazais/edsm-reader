import json
from datetime import datetime
from typing import Optional

import structlog
from astraeus_common.decorator.logit import logit
from astraeus_common.io.database import Database
from astraeus_common.models.system import System


class SystemService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_system_by_key(self, key: dict) -> Optional[System]:
        raw_data = self._io_db.exec_db_read(System.SYSTEM_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return System(raw_data[0])
        else:
            self._log.debug(f'No {System.__name__} found')
            return None

    @logit
    def create_system(self, system: System) -> None:
        system.update_time = datetime.now()
        self._io_db.exec_db_write(System.SYSTEM_INSERT, system.to_dict_for_db())

    @logit
    def update_system_by_key(self, system: System) -> None:
        system.update_time = datetime.now()
        self._io_db.exec_db_write(System.SYSTEM_UPDATE_BY_KEY, system.to_dict_for_db())

    @logit
    def delete_system_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(System.SYSTEM_DELETE_BY_KEY, {'key': json.dumps(key)})
