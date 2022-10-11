from datetime import datetime


class System:
    _key: dict
    _name: str
    _coordinates: dict
    _require_permit: bool
    _information: dict
    _update_time: datetime
    _primary_star: dict

    @property
    def key(self) -> dict:
        return self._key

    @key.setter
    def key(self, value: dict):
        self._key = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def coordinates(self) -> dict:
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: dict):
        self._coordinates = value

    @property
    def require_permit(self) -> bool:
        return self._require_permit

    @require_permit.setter
    def require_permit(self, value: bool):
        self._require_permit = value

    @property
    def information(self) -> dict:
        return self._information

    @information.setter
    def information(self, value: dict):
        self._information = value

    @property
    def update_time(self) -> datetime:
        return self._update_time

    @update_time.setter
    def update_time(self, value: datetime):
        self._update_time = value

    @property
    def primary_star(self) -> dict:
        return self._primary_star

    @primary_star.setter
    def primary_star(self, value: dict):
        self._primary_star = value

    def __init__(self,
                 dict_from_db: dict = None,
                 key: dict = None,
                 name: str = None,
                 coordinates: dict = None,
                 require_permit: bool = None,
                 information: dict = None,
                 update_time: datetime = None,
                 primary_star: dict = None):
        if dict_from_db is not None:
            key = dict_from_db['key']
            name = dict_from_db['name']
            coordinates = dict_from_db['coordinates']
            require_permit = dict_from_db['require_permit']
            information = dict_from_db['information']
            update_time = dict_from_db['update_time']
            primary_star = dict_from_db['primary_star']
        self._key = key
        self._name = name
        self._coordinates = coordinates
        self._require_permit = require_permit
        self._information = information
        self._update_time = update_time
        self._primary_star = primary_star

    def to_dict(self) -> dict:
        return {
            'key': self._key,
            'name': self._name,
            'coordinates': self._coordinates,
            'require_permit': self._require_permit,
            'information': self._information,
            'update_time': self._update_time,
            'primary_star': self._primary_star,
        }
