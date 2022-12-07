import json
from datetime import datetime
from typing import Optional

import structlog

from ..decorator.logit import logit
from ..io.database import Database
from ..models.system import System

SYSTEM_SELECT_BY_KEY = '''
select key, name, coordinates, require_permit, 
information, update_time, primary_star
from system
where key = %(key)s
'''

SYSTEM_INSERT = '''
insert into system 
(key, name, coordinates, require_permit, 
information, update_time, primary_star)
values 
(%(key)s,%(name)s,%(coordinates)s,%(require_permit)s,
%(information)s,%(update_time)s,%(primary_star)s);
'''

SYSTEM_UPDATE_BY_KEY = '''
update system 
set name = %(name)s,
    coordinates = %(coordinates)s,
    require_permit = %(require_permit)s,
    information = %(information)s,
    update_time = %(update_time)s,
    primary_star = %(primary_star)s
where key = %(key)s
'''

SYSTEM_DELETE_BY_KEY = '''
delete from system where key = %(key)s
'''


class SystemService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_system_by_key(self, key: dict) -> Optional[System]:
        raw_data = self._io_db.exec_db_read(SYSTEM_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return System(raw_data[0])
        else:
            self._log.debug(f'No {System.__name__} found')
            return None

    @logit
    def create_system(self, system: System) -> None:
        system.update_time = datetime.now()
        self._io_db.exec_db_write(SYSTEM_INSERT, system.to_dict_for_db())

    @logit
    def update_system_by_key(self, system: System) -> None:
        system.update_time = datetime.now()
        self._io_db.exec_db_write(SYSTEM_UPDATE_BY_KEY, system.to_dict_for_db())

    @logit
    def delete_system_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(SYSTEM_DELETE_BY_KEY, {'key': json.dumps(key)})
