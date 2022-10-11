from ..error.sync_state_not_found import SyncStateNotFound
from ..io.database import Database
from ..model.sync_state import SyncState

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
    sync_hash = %(sync_hash)s
where key = %(key)s
'''

SYNC_STATE_DELETE_BY_KEY = '''
delete from sync_state where key = %(key)s
'''


class SyncStateService:
    io_db: Database

    def __init__(self, db: Database):
        self.io_db = db

    def read_sync_state_by_key(self, key: dict) -> SyncState:
        raw_data = self.io_db.exec_db_read(SYNC_STATE_SELECT_BY_KEY, key)
        if len(raw_data) == 1:
            return SyncState(raw_data[0])
        else:
            raise SyncStateNotFound()

    def create_sync_state(self, sync_state: SyncState) -> None:
        self.io_db.exec_db_write(SYNC_STATE_INSERT, sync_state.to_dict())

    def update_sync_state_by_key(self, sync_state: SyncState) -> None:
        self.io_db.exec_db_write(SYNC_STATE_UPDATE_BY_KEY, sync_state.to_dict())

    def delete_sync_state_by_key(self, key: dict) -> None:
        self.io_db.exec_db_write(SYNC_STATE_DELETE_BY_KEY, key)
