from datetime import datetime


class SyncState:
    _key: dict
    _sync_date: datetime
    _type: str
    _sync_hash: str

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

    def __init__(self, dict_from_db: dict = None,
                 key: dict = None,
                 sync_date: datetime = None,
                 data_type: str = None,
                 sync_hash: str = None):
        if dict_from_db is not None:
            key = dict_from_db['key']
            sync_date = dict_from_db['sync_date']
            data_type = dict_from_db['data_type']
            sync_hash = dict_from_db['sync_hash']
        self._key = key
        self._sync_date = sync_date
        self._type = data_type
        self._sync_hash = sync_hash

    def to_dict(self) -> dict:
        return {
            'key': self._key,
            'sync_date': self._sync_date,
            'type': self._type,
            'sync_hash': self._sync_hash,
        }
