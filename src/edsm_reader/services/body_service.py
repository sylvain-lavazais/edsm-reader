import json
from datetime import datetime
from typing import Optional

import structlog

from astraeus_common.decorator.logit import logit
from astraeus_common.error.body_not_found import BodyNotFound
from astraeus_common.io.database import Database
from astraeus_common.models.body import Body


class BodyService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_body_by_key(self, key: dict) -> Optional[Body]:
        """
        Reads the body from the database using the given key.

        :param key: The key to search for in the database.
        :type key: Dict
        :return: The body if found, otherwise None.
        :rtype: Optional[Body]
        """
        raw_data = self._io_db.exec_db_read(Body.BODY_SELECT_BY_KEY, {'key': json.dumps(key)})
        if raw_data is not None and len(raw_data) > 0:
            return Body(raw_data[0])
        else:
            self._log.debug(f'No {Body.__name__} found')
            return None

    @logit
    def read_body_by_system_key(self, system_key: dict) -> Body:
        """
        Retrieve a Body by its system key.

        :param system_key: The system is key to the Body.
        :type system_key: Dict
        :return: The retrieved Body.
        :rtype: Body
        :raises BodyNotFound: If the Body with the specified system key is not found.
        """
        raw_data = self._io_db.exec_db_read(Body.BODY_SELECT_BY_SYSTEM_KEY, system_key)
        if len(raw_data) == 1:
            return Body(raw_data[0])
        else:
            raise BodyNotFound()

    @logit
    def create_body(self, body_created: Body) -> None:
        """
        Create a new body in the system.

        :param body_created: The body object to create.
        """
        body_created.update_time = datetime.now()
        self._io_db.exec_db_write(Body.BODY_INSERT, body_created.to_dict_for_db())

    @logit
    def update_body_by_key(self, body_created: Body) -> None:
        """
        Update the `body_created` object in the database by its key.

        :param body_created: The `Body` object to update.
        :type body_created: Body
        """
        body_created.update_time = datetime.now()
        self._io_db.exec_db_write(Body.BODY_UPDATE_BY_KEY, body_created.to_dict_for_db())

    @logit
    def delete_body_by_key(self, key: dict) -> None:
        """
        Deletes a body record from the database by the given key.

        :param key: The key used to identify the body record.
        :type key: Dict
        """
        self._io_db.exec_db_write(Body.BODY_DELETE_BY_KEY, {'key': json.dumps(key)})
