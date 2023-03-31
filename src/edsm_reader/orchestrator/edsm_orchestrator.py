import hashlib
import json
from threading import Thread, current_thread
from typing import List, Optional

import structlog
from astraeus_common.decorator.logit import logit
from astraeus_common.io.database import Database
from astraeus_common.models.body import body_from_edsm
from astraeus_common.models.sync_state import SyncState
from astraeus_common.models.system import system_from_edsm
from astraeus_common.utils.thread_safe_list import ThreadSafeList

from ..client.edsm_client import EdsmClient
from ..services.body_service import BodyService
from ..services.sync_state_service import SyncStateService
from ..services.system_service import SystemService
from ..utils.coordinate import Coordinate


class EdsmOrchestrator:
    _state_service: SyncStateService
    _body_service: BodyService
    _system_service: SystemService
    _edsm_client: EdsmClient

    def __init__(self, db: Database):
        self._state_service = SyncStateService(db)
        self._body_service = BodyService(db)
        self._system_service = SystemService(db)

        self._edsm_client = EdsmClient()

        self._log = structlog.get_logger()

    @logit
    def full_scan_from_coord(self, x_coord: int, y_coord: int, z_coord: int):
        scans_done = ThreadSafeList()
        system_already_registered = ThreadSafeList()
        self.__recursive_system_scan_from_coord(system_already_registered,
                                                scans_done,
                                                x_coord,
                                                y_coord,
                                                z_coord,
                                                100)

    @logit
    def refresh_system_list(self, data: List[dict]) -> None:
        for elem in data:
            self.refresh_a_full_system(elem, init=True)

    @logit
    def refresh_a_full_system(self, data: dict, init: bool = False) -> None:
        key = {'id': data['id'], 'id64': data['id64']}
        self._log.info(f'Processing system {key}')
        if init and self._state_service.read_sync_state_by_key(key) is not None:
            return
        self.__refresh_system_entity(key)
        self.__refresh_bodies_entities(key)

    def __recursive_system_scan_from_coord(self,
                                           system_already_registered: ThreadSafeList,
                                           scans_done: ThreadSafeList,
                                           x_coord: int,
                                           y_coord: int,
                                           z_coord: int,
                                           radius: int):
        scans_done.append((x_coord, y_coord, z_coord))
        systems = self._edsm_client.search_systems_from_coord(x_coord, y_coord, z_coord, radius)
        self._log.info(f'{current_thread()} - => Processing system search '
                       f'on x:{x_coord}, y:{y_coord}, z:{z_coord}')

        threads = []
        for system in systems:
            self.__register_system_and_bodies(system, system_already_registered)
            self.__add_sub_thread(radius, scans_done, system, system_already_registered, threads,
                                  x_coord, y_coord, z_coord)

        self._log.info(f'{current_thread()} - {len(threads)} sub-thread created')

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def __register_system_and_bodies(self, system, system_already_registered):
        key = {'id': system['id'], 'id64': system['id64']}
        if key not in system_already_registered:
            self._log.info(f'{current_thread()} - system {system["name"]} '
                           f'not scanned yet')
            self.__refresh_system_entity(key, system)
            self.__refresh_bodies_entities(key)
            system_already_registered.append(key)
        else:
            self._log.debug(f'{current_thread()} - system {system["name"]} '
                            f'has already been scanned')

    def __add_sub_thread(self, radius, scans_done, system, system_already_registered, threads,
                         x_coord, y_coord, z_coord):
        if 'coords' in system:
            coords = system['coords']
            if Coordinate(coords['x'], coords['y'], coords['z']) \
                    .is_outside_limit(x_coord, y_coord, z_coord, radius - 10):
                if (coords['x'], coords['y'], coords['z']) not in scans_done:
                    threads.append(Thread(target=self.__recursive_system_scan_from_coord,
                                          args=(system_already_registered,
                                                scans_done,
                                                coords['x'],
                                                coords['y'],
                                                coords['z'],
                                                radius)))
                    self._log.info(f'{current_thread()} - system {system["name"]} '
                                   f'not searched yet')
                else:
                    self._log.debug(f'{current_thread()} - system {system["name"]} '
                                    f'has already been searched')

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
                        previous_body_state = self.__update_create_body(key, body_key, edsm_body)
                        self.__update_sync_state(edsm_body_hash, body_key, 'body',
                                                 previous_body_state)

                else:
                    body = body_from_edsm(edsm_body)
                    body.system_key = key
                    self._body_service.create_body(body)
                    self.__create_sync_state(edsm_body, body_key, 'body')

    def __refresh_system_entity(self, key: dict, system: dict = None):
        sync_state = self._state_service.read_sync_state_by_key(key)
        if system is None:
            edsm_system: dict = self._edsm_client.get_system_from_system_id(key['id'])
        else:
            edsm_system: dict = system

        if len(edsm_system) > 0:
            if sync_state is not None:
                edsm_sys_hash = self.__compute_hash_of_dict(edsm_system)

                if edsm_sys_hash != sync_state.sync_hash:
                    previous_system_state = self.__update_create_system(key, edsm_system)
                    self._log.info(f'prev : {previous_system_state}')
                    self.__update_sync_state(edsm_sys_hash, key, 'system', previous_system_state)

            else:
                self._system_service.create_system(system_from_edsm(edsm_system))
                self.__create_sync_state(edsm_system, key, 'system')

    def __update_create_body(self,
                             system_key: dict,
                             body_key: dict,
                             edsm_body: dict) -> Optional[dict]:
        body = self._body_service.read_body_by_key(body_key)

        if body is not None:
            previous_state = body.to_dict_for_db()
            update_body = body_from_edsm(edsm_body)
            update_body.system_key = system_key
            self._body_service.update_body_by_key(update_body)
            return previous_state

        else:
            create_body = body_from_edsm(edsm_body)
            create_body.system_key = system_key
            self._body_service.create_body(create_body)

        return None

    def __update_create_system(self, key: dict, edsm_system: dict) -> Optional[dict]:
        system = self._system_service.read_system_by_key(key)
        if system is not None:

            previous_state = system.to_dict()
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
