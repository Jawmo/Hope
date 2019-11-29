import copy
from engine.global_config import *

from engine.update_client import Update_Client
from engine.handler.input_handler import Input_Handler
from engine.status_check import Status_Check

from websocket_server.wswrap import WsWrap

from engine.character import Character
from engine.lex import Lex
from engine.inventory import inv

from pprint import pprint

###### Player Class ######

class Player(Character):
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

        self.entity_type =      kwargs['entity_type']
        self.core_attributes =  kwargs['core_attributes']
        self.player_state =     kwargs['player_state']
        self.stow_loc =         kwargs['stow_loc']
        self.client =           kwargs['client']
        self.unique_id =        kwargs['unique_id']

    def display_inventory(self):

        inv = []

        for i in self.inventory:
            if self.inventory[i]['contents'] == None:
                pass
            else:
                inv.append("{} {} {} {}".format(self.inventory[i]['contents'].name, 
                                                self.inventory[i]['worn'], 
                                                "your", 
                                                self.inventory[i]['name']))
        
        if inv == []:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You have nothing.")   
        else:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You have {}.".format(", ".join(Lex.converted_contents(inv))))

        # WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, rooms[room_num].name)

    def echo(self):

        if self.conditions['echo'] == True:
            self.conditions['echo'] = False
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Echo is now |alert| disabled. |alertx|")
        else:
            self.conditions['echo'] = True
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Echo is now |success| enabled. |successx|")

    def help(self, user_input, input_kwargs):

        if len(user_input) < 2:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "|alert| Syntax: |alertx| HELP ON or HELP OFF.")

        else:

            if user_input[1] == "on":
                 WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, 'Help is |success| ON.|successx|')
                 self.conditions['help'] = "enabled"

            elif user_input[1] == "off":
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, 'Help is |alert| OFF|alertx|. ')
                self.conditions['help'] = "disabled"
                
            else:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "|alert| Syntax: |alertx| HELP ON or HELP OFF.")

    def stow_set(self, user_input, input_kwargs):
        
        stow_item = False

        if len(user_input) == 1 or len(user_input) > 3:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Syntax: STOW SET (container) or STOW (ITEM)")   

        elif user_input[1] == "set":
            
            input_kwargs['target'] = Input_Handler.target_self_inventory(self, user_input[2], input_kwargs)
            self.stow_loc = input_kwargs['target']
            
            if self.stow_loc == None:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Make sure you are wearing the container.")
            else:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Ok.")

        elif user_input[1] != "set":

            if self.stow_loc == None:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You must first STOW SET (CONTAINER) for a container you are wearing.")

            elif self.stow_loc.location_body['state'] != "worn":
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You must be wearing that container.")

            elif self.inventory['r_hand']['contents'] != None:
                if user_input[1] in self.inventory['r_hand']['contents'].name:
                    stow_item = True
                    input_kwargs['target'] = self.inventory['r_hand']['contents']
                    input_kwargs['target_parent'] = self.stow_loc
                    
            elif self.inventory['l_hand']['contents'] != None:
                if user_input[1] in self.inventory['l_hand']['contents'].name:
                    stow_item = True
                    input_kwargs['target'] = self.inventory['l_hand']['contents']
                    input_kwargs['target_parent'] = self.stow_loc

            else:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't stow that.")
           
            if stow_item == True:
                status, response = Status_Check.item_open_closed(self, user_input, input_kwargs)
                
                if status == True:
                    if self.stow_loc == input_kwargs['target']:
                        WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't stow something in itself.")
                    else:
                        Character.put_item(self, user_input, input_kwargs)
                else:
                    WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That is not open.")

        else:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Error with STOW target.")

    def target_player(self):
        # for i in server.clients:
        #     if i['id']
        pass

    def convert_players_to_obj():

        inventory = copy.deepcopy(inv)

        for i in players:
            print(players[i])
            new_player = Player(i,                  # uuid_id
                                players[i][0],      # entity_type
                                players[i][1],      # name
                                players[i][2],      # race
                                players[i][3],      # gender
                                players[i][4],      # vitals
                                players[i][5],      # core_attributes
                                players[i][6],      # conditions
                                players[i][7],      # credit
                                inventory,          # inventory
                                players[i][8],      # location
                                players[i][9],      # player_state
                                players[i][10],     # stow_loc
                                None,               # client
                                players[i][11])     # client_id / unique_id  
            
            players[i] = new_player
            print(vars(new_player))
            # pprint(vars(new_player))

    def list(self):
        print("Server.clients:", server.clients)