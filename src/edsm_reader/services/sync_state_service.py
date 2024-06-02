import json
from datetime import datetime
from typing import Optional

import structlog
from astraeus_common.decorator.logit import logit
from astraeus_common.io.database import Database
from astraeus_common.models.sync_state import SyncState


class SyncStateService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_sync_state_by_key(self, key: dict) -> Optional[SyncState]:
        """
        Reads the sync state by key.

        :param key: A dictionary representing the key to query for the sync state.
        :return: An optional `SyncState` object if the sync state is found, otherwise returns `None`.
        """
        raw_data = self._io_db.exec_db_read(SyncState.SYNC_STATE_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return SyncState(raw_data[0])
        else:
            self._log.debug(f'No {SyncState.__name__} found')
            return None

    @logit
    def create_sync_state(self, sync_state: SyncState) -> None:
        """
        Create a sync state in the database.

        :param sync_state: The sync state object to be created in the database.
        :type sync_state: SyncState
        """
        sync_state.sync_date = datetime.now()
        self._io_db.exec_db_write(SyncState.SYNC_STATE_INSERT, sync_state.to_dict_for_db())

    @logit
    def update_sync_state(self, sync_state: SyncState) -> None:
        """
        Update the sync state.

        :param sync_state: The sync state object to be updated.
        :type sync_state: SyncState
        """
        sync_state.sync_date = datetime.now()
        self._io_db.exec_db_write(SyncState.SYNC_STATE_UPDATE_BY_KEY, sync_state.to_dict_for_db())

    @logit
    def delete_sync_state_by_key(self, key: dict) -> None:
        """
        Delete the sync state by key.

        :param key: The key for the sync state to be deleted.
        """
        self._io_db.exec_db_write(SyncState.SYNC_STATE_DELETE_BY_KEY, {'key': json.dumps(key)})
