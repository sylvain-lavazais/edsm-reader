import structlog

from ..client.eddn_client import EddnClient
from ..decorator.logit import logit
from ..io.database import Database
from ..models.eddn_msg import EddnMsg
from ..services.body_service import BodyService
from ..services.eddn_msg_service import EddnMessageService
from ..services.sync_state_service import SyncStateService
from ..services.system_service import SystemService


class EddnOrchestrator:
    _state_service: SyncStateService
    _body_service: BodyService
    _system_service: SystemService
    _eddn_msg_service: EddnMessageService
    _eddn_client: EddnClient

    def __init__(self, db: Database):
        self._state_service = SyncStateService(db)
        self._body_service = BodyService(db)
        self._system_service = SystemService(db)
        self._eddn_msg_service = EddnMessageService(db)

        self._eddn_client = EddnClient()

        self._log = structlog.getLogger()

    def run_listener(self) -> None:
        self._eddn_client.run(self.__process_message)

    @logit
    def __process_message(self, msg: dict) -> None:
        self._log.info(f'Recording message')
        self._eddn_msg_service.create_eddn_message(
                EddnMsg(schema=msg['$schemaRef'],
                        header=msg['header'],
                        message=msg['message']))
