import json
import os

import click

from io.database import Database
from io.file import File

from services.system_service import SystemService
from error.system_not_found import SystemNotFound


class EDSMReader:
    api_key: str
    commander_name: str
    system_service: SystemService
    file_tools: File

    def __init__(self, api_key: str, commander_name: str, init_file_path: str):
        self.api_key = api_key
        self.commander_name = commander_name
        database = self.__build_db_from_param()
        self.system_service = SystemService(database)
        self.file_tools = File(init_file_path)

    def __build_db_from_param(self):
        db_host = os.getenv("DB_HOST", default="localhost")
        db_port = os.getenv("DB_PORT", default="5432")
        db_user = os.getenv("DB_USER", default="edsm-mirror")
        db_name = os.getenv("DB_NAME", default="edsm-mirror")
        db_password = os.getenv("DB_PASSWORD", default="edsm-mirror")
        database = Database(db_host, db_port, db_user, db_name, db_password)
        return database

    def init_sync_from_edsm(self):
        print('-> Reading file...')
        json_data = self.file_tools.read_json_file()
        print(f'-> Reading file done {len(json_data)} entries')
        for elem in json_data:
            if "id" in elem and "id64" in elem:
                key = json.dumps({'id': elem['id'], 'id64': elem['id64']})
                print(f'--> Reading {key} in sync db')

@click.command(no_args_is_help=True)
@click.option('--api_key', help="The EDSM api key")
@click.option('--commander_name', help="The EDSM registered commander name")
@click.option('--init_file_path', help="The file path to the system json file for init")
def command_line(api_key: str, commander_name: str, init_file_path: str):
    """Start the edsm reader application

    example: python __main__.py --api_key [key] --commander_name [name]
    """
    print(f'=== Starting {EDSMReader.__name__} ===')
    edsm_reader = EDSMReader(api_key, commander_name, init_file_path)
    edsm_reader.init_sync_from_edsm()


if __name__ == '__main__':
    command_line()
