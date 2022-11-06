import logging
import os
from threading import Thread

import click
import structlog as structlog

from .io.database import Database
from .io.file import File
from .orchestrator.eddn_orchestrator import EddnOrchestrator
from .orchestrator.edsm_orchestrator import EdsmOrchestrator


class EDSMReader:
    _orchestrator: EdsmOrchestrator
    _file_tools: File = None
    _parameters: dict
    _init_thread: Thread

    def __init__(self, api_key: str, commander_name: str, log_level: str,
                 init_file_path: str = None):
        self._parameters = {}
        database = self.__build_db_from_param()
        self._orchestrator = EdsmOrchestrator(database, api_key, commander_name)
        self._eddn_orchestrator = EddnOrchestrator(database)
        if init_file_path is not None:
            self._file_tools = File(init_file_path)

        structlog.configure(
                wrapper_class=structlog.make_filtering_bound_logger(
                        logging.getLevelName(log_level)),
        )
        self._log = structlog.get_logger()

        self._parameters.update({
                'api_key'       : api_key,
                'commander_name': commander_name,
                'init_file_path': init_file_path,
                'log_level'     : log_level
        })

    def __build_db_from_param(self):
        db_host = os.getenv("DB_HOST", default="localhost")
        db_port = os.getenv("DB_PORT", default="5432")
        db_user = os.getenv("DB_USER", default="edsm-mirror")
        db_name = os.getenv("DB_NAME", default="edsm-mirror")
        db_password = os.getenv("DB_PASSWORD", default="edsm-mirror")
        database = Database(db_host, db_port, db_user, db_name, db_password)

        self._parameters.update({
                'db_host'    : db_host,
                'db_port'    : db_port,
                'db_user'    : db_user,
                'db_name'    : db_name,
                'db_password': '*************',
        })

        return database

    def run(self):
        self._log.debug(f'===  Starting parameters')
        for key in self._parameters:
            self._log.debug(f'===  {key}: {self._parameters[key]}')

        if self._file_tools is not None:
            self._file_tools.read_json_file_and_exec(self._orchestrator.refresh_system_list)

        self._orchestrator.full_scan_from_coord(0, 0, 0)  # start scan from `Sol` system


@click.command(no_args_is_help=True)
@click.option('--api_key', help="The EDSM api key")
@click.option('--commander_name', help="The EDSM registered commander name")
@click.option('--init_file_path', help="The file path to the system json file for init")
@click.option('--log_level', help="The log level for trace")
def command_line(api_key: str, commander_name: str, init_file_path: str, log_level: str):
    """Start the edsm reader application

    example:
    python -m edsm-reader \
    --api_key [<your api_key>] \
    --commander_name [name] \
    --init_file_path [path/to/file] \
    --log_level [CRITICAL|ERROR|WARNING|INFO|DEBUG]
    """
    print(f'=== Starting {EDSMReader.__name__} ===')
    edsm_reader = EDSMReader(api_key, commander_name, log_level, init_file_path)
    edsm_reader.run()


if __name__ == '__main__':
    command_line()
