import json
from datetime import datetime
from typing import Optional

import structlog

from ..decorator.logit import logit
from ..io.database import Database
from ..models.sync_state import SyncState

SYNC_STATE_SELECT_BY_KEY = '''
select key, sync_date, type, sync_hash
from sync_state
where key = %(key)s
'''

SYNC_STATE_INSERT = '''
insert into sync_state
(key, sync_date, type, sync_hash)
values (%(key)s, %(sync_date)s, %(type)s, %(sync_hash)s)
'''

SYNC_STATE_UPDATE_BY_KEY = '''
update sync_state
set sync_date = %(sync_date)s,
    type = %(type)s,
    sync_hash = %(sync_hash)s,
    previous_state = %(previous_state)s
where key = %(key)s
'''

SYNC_STATE_DELETE_BY_KEY = '''
delete from sync_state where key = %(key)s
'''


class SyncStateService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_sync_state_by_key(self, key: dict) -> Optional[SyncState]:
        raw_data = self._io_db.exec_db_read(SYNC_STATE_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return SyncState(raw_data[0])
        else:
            self._log.debug(f'No {SyncState.__name__} found')
            return None

    @logit
    def create_sync_state(self, sync_state: SyncState) -> None:
        sync_state.sync_date = datetime.now()
        self._io_db.exec_db_write(SYNC_STATE_INSERT, sync_state.to_dict_for_db())

    @logit
    def update_sync_state(self, sync_state: SyncState) -> None:
        sync_state.sync_date = datetime.now()
        self._io_db.exec_db_write(SYNC_STATE_UPDATE_BY_KEY, sync_state.to_dict_for_db())

    @logit
    def delete_sync_state_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(SYNC_STATE_DELETE_BY_KEY, {'key': json.dumps(key)})
