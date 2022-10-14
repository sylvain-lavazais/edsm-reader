import hashlib
import json
from datetime import datetime
from typing import Optional

import structlog

from .body_service import BodyService
from .system_service import SystemService
from ..client.edsm_client import EdsmClient
from ..decorator.logit import logit
from ..io.database import Database
from ..model.sync_state import SyncState
from ..model.system import from_edsm

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
    _edsm_client: EdsmClient
    _io_db: Database
    _system_service: SystemService
    _body_service: BodyService

    def __init__(self, db: Database, api_key: str, commander_name: str):
        self._io_db = db
        self._system_service = SystemService(db)
        self._body_service = BodyService(db)
        self._edsm_client = EdsmClient(api_key, commander_name)
        self._log = structlog.get_logger()

    @logit
    def read_sync_state_by_key(self, key: dict) -> Optional[SyncState]:
        raw_data = self._io_db.exec_db_read(SYNC_STATE_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None:
            return SyncState(raw_data[0])
        else:
            self._log.warn("No sync-state found")
            return None

    @logit
    def create_sync_state(self, sync_state: SyncState) -> None:
        self._io_db.exec_db_write(SYNC_STATE_INSERT, sync_state.to_dict_for_db())

    @logit
    def update_sync_state_by_key(self, sync_state: SyncState) -> None:
        self._io_db.exec_db_write(SYNC_STATE_UPDATE_BY_KEY, sync_state.to_dict_for_db())

    @logit
    def delete_sync_state_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(SYNC_STATE_DELETE_BY_KEY, key)

    @logit
    def refresh_one_sync_state(self, data: dict) -> None:
        '''
        Refresh a sync_state
        :param data: a json dict (from EDSM json file)
        :return: Nothing
        '''
        key: dict = {'id': data['id'], 'id64': data['id64']}
        sync_state: Optional[SyncState] = self.read_sync_state_by_key(key)
        edsm_system: dict = self._edsm_client.get_system_from_system_id(key['id'])

        if sync_state is not None:
            edsm_hash = self.__compute_hash_of_dict(edsm_system)
            if edsm_hash != sync_state.sync_hash:
                new_sync: SyncState = SyncState(
                    key=key,
                    sync_date=datetime.now(),
                    data_type='system',
                    sync_hash=edsm_hash,
                )
                system = self._system_service.read_system_by_key(key)

                if system is not None:
                    new_sync.previous_state = system.to_dict()
                    self._system_service.update_system_by_key(from_edsm(edsm_system))
                else:
                    self._system_service.create_system(from_edsm(edsm_system))

                self.update_sync_state_by_key(new_sync)
            else:
                self._log.info(f"hash is the same - No update to do on system [{data['name']}]")
        else:
            edsm_hash = self.__compute_hash_of_dict(edsm_system)
            sync: SyncState = SyncState(
                key=key,
                sync_date=datetime.now(),
                data_type='system',
                sync_hash=edsm_hash
            )
            self._system_service.create_system(from_edsm(edsm_system))
            self.create_sync_state(sync)

        # TODO: read if the hash of sync has changed (for each object of the system)
        # TODO: ex: 1 system, 20 bodies = 1 check on system, then 20 check of bodies
        # TODO: sync entities changes
        # TODO: for each syncdata refresh (change of hash or not), update sync_date

    def __compute_hash_of_dict(self, data: dict) -> str:
        result = hashlib.sha256(
            bytes(json.dumps(data, sort_keys=True, default=str), 'utf-8')).hexdigest()
        self._log.debug(f'hash of {data} = {result}')
        return result
