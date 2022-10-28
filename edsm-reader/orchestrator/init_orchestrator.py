import hashlib
import json
from typing import List, Optional

import structlog

from ..client.edsm_client import EdsmClient
from ..decorator.logit import logit
from ..io.database import Database
from ..models.body import body_from_edsm
from ..models.sync_state import SyncState
from ..models.system import system_from_edsm
from ..services.body_service import BodyService
from ..services.sync_state_service import SyncStateService
from ..services.system_service import SystemService


class InitOrchestrator:
    _state_service: SyncStateService
    _body_service: BodyService
    _system_service: SystemService
    _edsm_client: EdsmClient

    def __init__(self, db: Database, api_key: str, commander_name: str):
        self._state_service = SyncStateService(db)
        self._body_service = BodyService(db)
        self._system_service = SystemService(db)

        self._edsm_client = EdsmClient(api_key, commander_name)

        self._log = structlog.get_logger()

    @logit
    def refresh_system_list(self, data: List[dict]) -> None:
        for elem in data:
            self.refresh_a_full_system(elem)

    @logit
    def refresh_a_full_system(self, data: dict) -> None:
        key = {'id': data['id'], 'id64': data['id64']}
        self._log.info(f'Processing system {key}')
        self.__refresh_system_entity(key)
        self.__refresh_bodies_entities(key)

    def __refresh_bodies_entities(self, key: dict):
        edsm_bodies = self._edsm_client.get_bodies_from_system_id(key['id'])
        if len(edsm_bodies) > 0:
            self._log.info(f'=> Processing {len(edsm_bodies)} bodies for system {key}')

            for edsm_body in edsm_bodies:

                body_key = {'id': edsm_body['id'], 'id64': edsm_body['id64']}
                body_state = self._state_service.read_sync_state_by_key(body_key)

                if body_state is not None:
                    edsm_body_hash = self.__compute_hash_of_dict(edsm_body)

                    if edsm_body_hash != body_state.sync_hash:
                        previous_body_state = self.__update_create_body(body_key, edsm_body)
                        self.__update_sync_state(edsm_body_hash, body_key, 'body',
                                                 previous_body_state)

                else:
                    body = body_from_edsm(edsm_body)
                    body.system_key = key
                    self._body_service.create_body(body)
                    self.__create_sync_state(edsm_body, body_key, 'body')

    def __refresh_system_entity(self, key: dict):
        sync_state = self._state_service.read_sync_state_by_key(key)
        edsm_system = self._edsm_client.get_system_from_system_id(key['id'])

        if sync_state is not None:
            edsm_sys_hash = self.__compute_hash_of_dict(edsm_system)

            if edsm_sys_hash != sync_state.sync_hash:
                previous_system_state = self.__update_create_system(edsm_system, key)
                self.__update_sync_state(edsm_sys_hash, key, 'system', previous_system_state)

        else:

            self._system_service.create_system(system_from_edsm(edsm_system))
            self.__create_sync_state(edsm_system, key, 'system')

    def __update_create_body(self, body_key: dict, edsm_body: dict) -> Optional[dict]:
        body = self._body_service.read_body_by_key(body_key)

        if body is not None:
            previous_state = body.to_dict_for_db()
            self._body_service.update_body_by_key(body_from_edsm(edsm_body))
            return previous_state

        else:
            self._body_service.create_body(body_from_edsm(edsm_body))

        return None

    def __update_create_system(self, key: dict, edsm_system: dict) -> Optional[dict]:
        system = self._system_service.read_system_by_key(key)
        if system is not None:
            previous_state = system.to_dict_for_db()
            self._system_service.update_system_by_key(system_from_edsm(edsm_system))
            return previous_state

        else:
            self._system_service.create_system(system_from_edsm(edsm_system))

        return None

    def __update_sync_state(self, object_hash: str, key_to_save: dict, data_type: str,
                            previous_state: dict = None) -> None:
        new_sync = SyncState(
                key=key_to_save,
                data_type=data_type,
                sync_hash=object_hash,
                previous_state=previous_state
        )
        self._state_service.update_sync_state(new_sync)

    def __create_sync_state(self, edsm_dict: dict, key_to_save: dict, data_type: str) -> None:
        sync = SyncState(
                key=key_to_save,
                data_type=data_type,
                sync_hash=self.__compute_hash_of_dict(edsm_dict)
        )
        self._state_service.create_sync_state(sync)

    def __compute_hash_of_dict(self, data: dict) -> str:
        result = hashlib.sha256(
                bytes(json.dumps(data, sort_keys=True, default=str), 'utf-8')).hexdigest()
        self._log.debug(f'hash of {data} = {result}')
        return result
