import logging
import os

import click
import structlog as structlog

from .io.database import Database
from .io.file import File
from .services.sync_state_service import SyncStateService


class EDSMReader:
    _sync_state_service: SyncStateService
    _file_tools: File

    def __init__(self, api_key: str, commander_name: str, init_file_path: str, log_level: str):
        database = self.__build_db_from_param()
        self._sync_state_service = SyncStateService(database, api_key, commander_name)
        self._file_tools = File(init_file_path)

        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level)),
        )
        self._log = structlog.get_logger()

    def __build_db_from_param(self):
        db_host = os.getenv("DB_HOST", default="localhost")
        db_port = os.getenv("DB_PORT", default="5432")
        db_user = os.getenv("DB_USER", default="edsm-mirror")
        db_name = os.getenv("DB_NAME", default="edsm-mirror")
        db_password = os.getenv("DB_PASSWORD", default="edsm-mirror")
        database = Database(db_host, db_port, db_user, db_name, db_password)
        return database

    def init_sync_from_edsm(self):
        self._log.info('Starting init database from file')
        self._file_tools.read_json_file_and_exec(self._sync_state_service.refresh_system_list)
        self._log.info('End of init...')


@click.command(no_args_is_help=True)
@click.option('--api_key', help="The EDSM api key")
@click.option('--commander_name', help="The EDSM registered commander name")
@click.option('--init_file_path', help="The file path to the system json file for init")
def command_line(api_key: str, commander_name: str, init_file_path: str):
    """Start the edsm reader application

    example: python __main__.py --api_key [key] --commander_name [name]
    """
    print(f'=== Starting {EDSMReader.__name__} ===')
    edsm_reader = EDSMReader(api_key, commander_name, init_file_path, 'INFO')
    edsm_reader.init_sync_from_edsm()


if __name__ == '__main__':
    command_line()
