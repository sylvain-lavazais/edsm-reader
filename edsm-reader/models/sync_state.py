import json
from datetime import datetime


class SyncState:
    _key: dict
    _sync_date: datetime
    _type: str
    _sync_hash: str
    _previous_state: dict

    @property
    def key(self) -> dict:
        return self._key

    @key.setter
    def key(self, value: dict):
        self._key = value

    @property
    def sync_date(self) -> datetime:
        return self._sync_date

    @sync_date.setter
    def sync_date(self, value: datetime):
        self._sync_date = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def sync_hash(self) -> str:
        return self._sync_hash

    @sync_hash.setter
    def sync_hash(self, value: str):
        self._sync_hash = value

    @property
    def previous_state(self) -> dict:
        return self._previous_state

    @previous_state.setter
    def previous_state(self, value: dict):
        self._previous_state = value

    def __init__(self, dict_from_db: dict = None,
                 key: dict = None,
                 sync_date: datetime = None,
                 data_type: str = None,
                 sync_hash: str = None,
                 previous_state: dict = None):
        if dict_from_db is not None:
            key = dict_from_db.get('key', None)
            sync_date = dict_from_db.get('sync_date', None)
            data_type = dict_from_db.get('type', None)
            sync_hash = dict_from_db.get('sync_hash', None)
            previous_state = dict_from_db.get('previous_state', None)
        self._key = key
        self._sync_date = sync_date
        self._type = data_type
        self._sync_hash = sync_hash
        self._previous_state = previous_state

    def to_dict(self) -> dict:
        return {
                'key'           : self._key,
                'sync_date'     : self._sync_date,
                'type'          : self._type,
                'sync_hash'     : self._sync_hash,
                'previous_state': self._previous_state
        }

    def to_dict_for_db(self) -> dict:
        return {
                'key'           : json.dumps(self._key),
                'sync_date'     : self._sync_date,
                'type'          : self._type,
                'sync_hash'     : self._sync_hash,
                'previous_state': json.dumps(self._previous_state, default=str)
        }
