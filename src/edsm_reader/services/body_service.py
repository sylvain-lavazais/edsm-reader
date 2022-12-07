import json
from datetime import datetime
from typing import Optional

import structlog

from ..decorator.logit import logit
from ..error.body_not_found import BodyNotFound
from ..io.database import Database
from ..models.body import Body

BODY_SELECT_BY_KEY = '''
select key, system_key, name, type,
sub_type, discovery, update_time, materials,
solid_composition, atmosphere_composition, parents, belts,
rings, properties
from body
where key = %(key)s
'''

BODY_SELECT_BY_SYSTEM_KEY = '''
select key, system_key, name, type,
sub_type, discovery, update_time, materials,
solid_composition, atmosphere_composition, parents, belts,
rings, properties
from body
where system_key = %(system_key)s
'''

BODY_INSERT = '''
insert into body
(key, system_key, name, type,
sub_type, discovery, update_time, materials,
solid_composition, atmosphere_composition, parents,
belts, rings, properties)
values 
(%(key)s, %(system_key)s, %(name)s, %(type)s,
%(sub_type)s, %(discovery)s, %(update_time)s, %(materials)s,
%(solid_composition)s, %(atmosphere_composition)s, %(parents)s,
%(belts)s, %(rings)s, %(properties)s)
'''

BODY_UPDATE_BY_KEY = '''
update body
set system_key = %(system_key)s,
    name = %(name)s,
    type = %(type)s,
    sub_type = %(sub_type)s,
    discovery = %(discovery)s,
    update_time = %(update_time)s,
    materials = %(materials)s,
    solid_composition = %(solid_composition)s,
    atmosphere_composition = %(atmosphere_composition)s,
    parents = %(parents)s,
    belts = %(belts)s,
    rings = %(rings)s,
    properties = %(properties)s
where key = %(key)s
'''

BODY_DELETE_BY_KEY = '''
delete from body where key = %(key)s
'''


class BodyService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_body_by_key(self, key: dict) -> Optional[Body]:
        raw_data = self._io_db.exec_db_read(BODY_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return Body(raw_data[0])
        else:
            self._log.debug(f'No {Body.__name__} found')
            return None

    @logit
    def read_body_by_system_key(self, system_key: dict) -> Body:
        raw_data = self._io_db.exec_db_read(BODY_SELECT_BY_SYSTEM_KEY, system_key)
        if len(raw_data) == 1:
            return Body(raw_data[0])
        else:
            raise BodyNotFound()

    @logit
    def create_body(self, body: Body) -> None:
        body.update_time = datetime.now()
        self._io_db.exec_db_write(BODY_INSERT, body.to_dict_for_db())

    @logit
    def update_body_by_key(self, body: Body) -> None:
        body.update_time = datetime.now()
        self._io_db.exec_db_write(BODY_UPDATE_BY_KEY, body.to_dict_for_db())

    @logit
    def delete_body_by_key(self, key: dict) -> None:
        self._io_db.exec_db_write(BODY_DELETE_BY_KEY, {'key': json.dumps(key)})
