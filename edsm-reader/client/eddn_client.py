import json
import time
import zlib
from typing import Callable

import structlog
import zmq

RELAY_ADDRESS = 'tcp://eddn.edcd.io:9500'
RELAY_TIMEOUT = 600000


class EddnClient:

    def __init__(self):
        self._context = zmq.Context()
        self._subscriber = self._context.socket(zmq.SUB)

        self._subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        self._subscriber.setsockopt(zmq.RCVTIMEO, RELAY_TIMEOUT)

        self._log = structlog.getLogger()

    def run(self, function: Callable):
        while True:
            try:
                self._subscriber.connect(RELAY_ADDRESS)

                while True:
                    raw_message = self._subscriber.recv()

                    if not raw_message:
                        self._log.debug(f'No new message from EDDN')
                        self._subscriber.disconnect(RELAY_ADDRESS)
                        break
                    self._log.debug(f'Receiving a new message from EDDN')

                    eddn_message = json.loads(zlib.decompress(raw_message))

                    function(eddn_message)

            except zmq.ZMQError as e:
                self._log.error(f'Error on EDDN accessor {str(e)}')
                self._subscriber.disconnect(RELAY_ADDRESS)
                time.sleep(5)
