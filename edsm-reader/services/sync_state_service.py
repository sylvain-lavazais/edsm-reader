import json

from .body_service import BodyService
from .system_service import SystemService
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
    system_service: SystemService
    body_service: BodyService

    def __init__(self, db: Database):
        self.io_db = db
        self.system_service = SystemService(db)
        self.body_service = BodyService(db)

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

    def refresh_one_sync_state(self, data: dict) -> None:
        '''
        Refresh a sync_state
        :param data: a json dict (from EDSM json file)
        :return: Nothing
        '''
        # TODO: read if sync exist, if not sync it (entities, then sync themselves)
        key: dict = {'id': data['id'], 'id64': data['id64']}

        # TODO: read if the hash of sync has changed (for each object of the system)
        # TODO: ex: 1 system, 20 bodies = 1 check on system, then 20 check of bodies
        # TODO: sync entities changes
        # TODO: for each syncdata refresh (change of hash or not), update sync_date

    def __compute_hash_of_dict(self, data: dict) -> str:
        return str(hash(json.dumps(data, sort_keys=True)))
