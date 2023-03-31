import logging
import os
from threading import Thread

import click
import structlog as structlog

from astraeus_common.io.database import Database

from .orchestrator.edsm_orchestrator import EdsmOrchestrator


class EDSMReader:
    _orchestrator: EdsmOrchestrator
    _parameters: dict
    _init_thread: Thread

    def __init__(self, log_level: str):
        if log_level is None:
            log_level = 'INFO'

        structlog.configure(
                wrapper_class=structlog.make_filtering_bound_logger(
                        logging.getLevelName(log_level)),
        )
        self._log = structlog.get_logger()

        self._parameters = {}
        database = self.__build_db_from_param()
        self._orchestrator = EdsmOrchestrator(database)

        self._parameters.update({
                'log_level': log_level
        })

    def __build_db_from_param(self):
        db_host = os.getenv("DB_HOST", default="localhost")
        db_port = os.getenv("DB_PORT", default="5432")
        db_user = os.getenv("DB_USER", default="astraeus")
        db_name = os.getenv("DB_NAME", default="astraeus-db")
        db_password = os.getenv("DB_PASSWORD", default="astraeus")
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
        self._log.debug('===  Starting parameters')
        for key in self._parameters:
            self._log.debug(f'===  {key}: {self._parameters[key]}')

        self._orchestrator.full_scan_from_coord(0, 0, 0)  # start scan from `Sol` system


@click.command()
@click.option('--log_level', help="The log level for trace")
def command_line(log_level: str = 'INFO'):
    """Start the edsm reader application

    example:
    edsm-reader -log_level [CRITICAL|ERROR|WARNING|INFO|DEBUG]
    """
    print(f'=== Starting {EDSMReader.__name__} ===')
    edsm_reader = EDSMReader(log_level)
    edsm_reader.run()
