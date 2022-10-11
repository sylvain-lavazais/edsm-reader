from ..error.system_not_found import SystemNotFound
from ..io.database import Database
from ..model.system import System

SYSTEM_SELECT_BY_KEY = '''
select key, name, coordinates, require_permit, 
information, update_time, primary_star
from system
where key = %(key)s
'''

SYSTEM_INSERT = '''
insert into system 
(key, name, coordinates, require_permit, 
information, update_time, primary_star)
values 
(%(key)s,%(name)s,%(coordinates)s,%(require_permit)s,
%(information)s,%(update_time)s,%(primary_star)s);
'''

SYSTEM_UPDATE_BY_KEY = '''
update system 
set name = %(name)s,
    coordinates = %(coordinates)s,
    require_permit = %(require_permit)s,
    information = %(information)s,
    update_time = %(update_time)s,
    primary_star = %(primary_star)s
where key = %(key)s
'''

SYSTEM_DELETE_BY_KEY = '''
delete from system where key = %(key)s
'''


class SystemService:
    io_db: Database

    def __init__(self, db: Database):
        self.io_db = db

    def read_system_by_key(self, key: dict) -> System:
        raw_data = self.io_db.exec_db_read(SYSTEM_SELECT_BY_KEY, key)
        if len(raw_data) == 1:
            return System(raw_data[0])
        else:
            raise SystemNotFound()

    def create_system(self, system: System) -> None:
        self.io_db.exec_db_write(SYSTEM_INSERT, system.to_dict())

    def update_system_by_key(self, system: System) -> None:
        self.io_db.exec_db_write(SYSTEM_UPDATE_BY_KEY, system.to_dict())

    def delete_system_by_key(self, key: dict) -> None:
        self.io_db.exec_db_write(SYSTEM_DELETE_BY_KEY, key)
