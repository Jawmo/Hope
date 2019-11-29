import json

from engine.global_config import *
from engine.handler.input_handler import Input_Handler

from websocket_server.wswrap import WsWrap

from engine.lex import Lex
from engine.player import Player
from engine.room import Room
from engine.npc import Npc
from engine.gen import Gen
from engine.item import Item

##### Other Functions #####

def look(self, user_input, input_kwargs):

    # This is the general look function. It allows a player to look at the room,
    # look at items, in items, etc. Basically anyhthing that invloves the 'look' 
    # verb.

    print("LOOK | UI:", user_input)
    if len(user_input) == 1:
        rooms[self.location].display_room(self)
    else:

        if user_input[1] == "at":

            # input_kwargs['target'] = Input_Handler.full_handler(self, user_input[2], input_kwargs)
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1},  "|alert| Syntax: |alertx| L  |  L (item)  |  L in (item).")

        elif user_input[1] == "in":
        
            input_kwargs['target'] = Input_Handler.full_handler(self, user_input[2], input_kwargs)
            print("LOOK | ", input_kwargs)

            if not input_kwargs['target']:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1},  "Look in what?")
            else:

                if not hasattr(input_kwargs['target'], "is_open"):
                    WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1},  "You can't really look in that.")
                else:

                    if input_kwargs['target'].is_open == False:
                        WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That is closed.")
                    else:
                        if input_kwargs['target'].entity_type['base'] == "item":
                            Item.items_in_item(self, user_input, input_kwargs)
                        else:
                            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't seem to do that.")

        else:

            input_kwargs['target'] = Input_Handler.full_handler(self, user_input[1], input_kwargs)
            
            print("LOOK | ", input_kwargs)

            if not input_kwargs['target']:
                
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That's not a valid target.")

            else:

                input_kwargs['target'].entity_description(self, user_input, input_kwargs)