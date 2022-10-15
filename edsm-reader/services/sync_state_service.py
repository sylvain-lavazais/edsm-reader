import hashlib
import json
from datetime import datetime
from typing import Optional, List

import structlog

from .body_service import BodyService
from .system_service import SystemService
from ..client.edsm_client import EdsmClient
from ..decorator.logit import logit
from ..io.database import Database
from ..model.body import body_from_edsm
from ..model.sync_state import SyncState
from ..model.system import system_from_edsm

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
        if raw_data is not None and len(raw_data) > 0:
            return SyncState(raw_data[0])
        else:
            self._log.debug("No sync-state found")
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
    def refresh_system_list(self, data: List[dict]) -> None:
        for elem in data:
            pass
            # self.refresh_one_system(elem)

    @logit
    def refresh_one_system(self, data: dict) -> None:
        '''
        Refresh a sync_state
        :param data: a json dict (from EDSM json file)
        :return: Nothing
        '''
        key: dict = {'id': data['id'], 'id64': data['id64']}
        self._log.info(f'Processing system {key}')
        sync_state: Optional[SyncState] = self.read_sync_state_by_key(key)
        edsm_system: dict = self._edsm_client.get_system_from_system_id(key['id'])

        if sync_state is not None:
            edsm_sys_hash = self.__compute_hash_of_dict(edsm_system)
            if edsm_sys_hash != sync_state.sync_hash:
                self.__update_system_and_state(edsm_sys_hash, edsm_system, key)
        else:
            self.__create_system_and_state(edsm_system, key)

        self.refresh_body_form_system_key(key)

    def refresh_body_form_system_key(self, key):
        edsm_bodies: List[dict] = self._edsm_client.get_bodies_from_system_id(key['id'])
        if len(edsm_bodies) > 0:
            self._log.info(f'=> Processing {len(edsm_bodies)} bodies for system {key}')
            for edsm_body in edsm_bodies:
                body_key: dict = {'id': edsm_body['id'], 'id64': edsm_body['id64']}
                body_state: Optional[SyncState] = self.read_sync_state_by_key(body_key)
                if body_state is not None:
                    edsm_body_hash = self.__compute_hash_of_dict(edsm_body)
                    if edsm_body_hash != body_state.sync_hash:
                        self.__update_body_and_state(body_key, edsm_body, edsm_body_hash)
                else:
                    self.__create_body_and_state(body_key, edsm_body, key)

    def __create_body_and_state(self, body_key, edsm_body, key):
        edsm_body_hash = self.__compute_hash_of_dict(edsm_body)
        sync: SyncState = SyncState(
            key=body_key,
            sync_date=datetime.now(),
            data_type='body',
            sync_hash=edsm_body_hash
        )
        body = body_from_edsm(edsm_body)
        body.system_key = key
        self._body_service.create_body(body)
        self.create_sync_state(sync)

    def __update_body_and_state(self, body_key, edsm_body, edsm_body_hash):
        new_body_sync: SyncState = SyncState(
            key=body_key,
            sync_date=datetime.now(),
            data_type='body',
            sync_hash=edsm_body_hash,
        )
        body = self._body_service.read_body_by_key(body_key)
        if body is not None:
            new_body_sync.previous_state = body.to_dict_for_db()
            self._body_service.update_body_by_key(body_from_edsm(edsm_body))
        else:
            self._body_service.create_body(body_from_edsm(edsm_body))
        self.update_sync_state_by_key(new_body_sync)

    def __create_system_and_state(self, edsm_system, key):
        edsm_hash = self.__compute_hash_of_dict(edsm_system)
        sync: SyncState = SyncState(
            key=key,
            sync_date=datetime.now(),
            data_type='system',
            sync_hash=edsm_hash
        )
        self._system_service.create_system(system_from_edsm(edsm_system))
        self.create_sync_state(sync)

    def __update_system_and_state(self, edsm_hash, edsm_system, key):
        new_sync: SyncState = SyncState(
            key=key,
            sync_date=datetime.now(),
            data_type='system',
            sync_hash=edsm_hash,
        )
        system = self._system_service.read_system_by_key(key)
        if system is not None:
            new_sync.previous_state = system.to_dict_for_db()
            self._system_service.update_system_by_key(system_from_edsm(edsm_system))
        else:
            self._system_service.create_system(system_from_edsm(edsm_system))
        self.update_sync_state_by_key(new_sync)

    def __compute_hash_of_dict(self, data: dict) -> str:
        result = hashlib.sha256(
            bytes(json.dumps(data, sort_keys=True, default=str), 'utf-8')).hexdigest()
        self._log.debug(f'hash of {data} = {result}')
        return result
