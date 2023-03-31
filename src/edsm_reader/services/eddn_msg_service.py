from datetime import datetime
from typing import Optional, List

import structlog
from astraeus_common.decorator.logit import logit
from astraeus_common.io.database import Database
from astraeus_common.models.eddn_msg import EddnMsg


class EddnMessageService:
    _io_db: Database

    def __init__(self, db: Database):
        self._io_db = db
        self._log = structlog.get_logger()

    @logit
    def read_eddn_message_by_id(self, uuid: str) -> Optional[EddnMsg]:
        raw_data = self._io_db.exec_db_read(EddnMsg.EDDN_MESSAGE_SELECT_BY_ID, {'id': uuid})
        if raw_data is not None and len(raw_data) > 0:
            return EddnMsg(raw_data[0])
        else:
            self._log.debug(f'No {EddnMsg.__name__} found')
            return None

    @logit
    def read_eddn_message_unread(self) -> Optional[List[EddnMsg]]:
        raw_data = self._io_db.exec_db_read(EddnMsg.EDDN_MESSAGE_SELECT_BY_ID)
        if raw_data is not None and len(raw_data) > 0:
            eddn_msgs = []
            for data in raw_data:
                eddn_msgs.append(EddnMsg(data))
            return eddn_msgs
        else:
            self._log.debug(f'No {EddnMsg.__name__} found')
            return None

    @logit
    def create_eddn_message(self, eddn_msg: EddnMsg) -> None:
        eddn_msg.recv_date = datetime.now()
        self._io_db.exec_db_write(EddnMsg.EDDN_MESSAGE_INSERT, eddn_msg.to_dict_for_db())

    @logit
    def update_eddn_message(self, eddn_msg: EddnMsg) -> None:
        self._io_db.exec_db_write(EddnMsg.EDDN_MESSAGE_UPDATE_BY_ID, eddn_msg.to_dict_for_db())

    @logit
    def delete_sync_state_by_id(self, uuid: str) -> None:
        self._io_db.exec_db_write(EddnMsg.EDDN_MESSAGE_DELETE_BY_ID, {'id': uuid})
