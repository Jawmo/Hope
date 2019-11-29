import sys, json, sched

from engine.global_config import *
from server_two import new_client, client_left, message_received

from engine.start import start


server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
start()
# initialize_sounds()
server.run_forever()