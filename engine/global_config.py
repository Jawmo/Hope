import sched, time, logging
from engine.scheduler import *
from engine.global_lists import *
from websocket_server.websocket_server import WebsocketServer

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format = '%(asctime)s %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    filename = 'main_log.log',
                    level=logging.DEBUG)

PORT=9001
server = WebsocketServer(PORT)
