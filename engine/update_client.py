import uuid

from engine.global_config import *

from engine.lex import Lex
from websocket_server.wswrap import WsWrap

# from engine.functions import *

class Update_Client():

    def __init__(self, core_attributes, vitals):
        pass
        # self.core_attributes = core_attributes
        # self.hp = vitals

        # self = player object
        # When a player logs in, this recurrent function will send the player
        # attributes to the client and put itself back in the queue to resend
        # to the client once per second.

    def update_map(self, map_render):

        send_kwargs = {'type': 'map_render', 'spacing': False}

        WsWrap.ws_send(self.client, send_kwargs, map_render)


    def update_char_info(self):

        send_kwargs = {'type': 'char_info', 'spacing': False}

        char_info = {}

        char_info['char_name'] = self.name.capitalize()
        char_info['char_gender'] = self.gender.capitalize()
        char_info['char_xp'] = self.core_attributes['xp']['current']

        # update health
        WsWrap.ws_send(self.client, send_kwargs, char_info)

    def update_init_round_time(self):

        send_kwargs = {'type': 'init_round_time', 'spacing': False}

        init_round_time = self.conditions['init_round_time'] 

        # update init rt
        try:
            WsWrap.ws_send(self.client, send_kwargs, init_round_time)
        except:
            print("ERROR | UPDATE INIT RT | Cannot update client for", self.name + ". User not in-game.")

    def update_round_time(self):

        send_kwargs = {'type': 'round_time', 'spacing': 1}

        round_time = self.conditions['round_time']

        # update rt
        try:
            print(self.client)
            WsWrap.ws_send(self.client, send_kwargs, round_time)
        except:
            print("ERROR | UPDATE RT | Cannot update client for", self.name + ". User not in-game.")

    def update_user_settings(self):

        send_kwargs = {'type': 'user_settings', 'spacing': False}

        user_settings = {}

        user_settings['player_name'] = self.name
        user_settings['location'] = self.location
        user_settings['player_state'] = self.player_state

        # update health
        WsWrap.ws_send(self.client, send_kwargs, user_settings)

    def update_player_list(self):

        send_kwargs = {'type': 'player_list', 'spacing': False}
        
        player_list = {}
        
        for player in players:
            player_list[players[player].name] = {'player_title'         :   players[player].core_attributes['title'], 
                                                 'player_name'          :   players[player].name, 
                                                 'entity_type'          :   players[player].entity_type['group'],
                                                 'player_state'         :   players[player].player_state}
        
        # update health
        server.send_message_to_all(send_kwargs, player_list)

        # # re-issue update command into scheduler queue
        # s.enterabs(time.time() + 1, 1, Client_Player_Update.update_player_health, kwargs=({'self': self}))

    def update_player_inventory(self):

        send_kwargs = {'type': 'inventory', 'spacing': False}
        
        # update health
        jinventory = {}

        for item in self.inventory:
            if self.inventory[item]['contents'] is not None:
                parsed_item = self.inventory[item]['contents'].name
                
                jinventory[self.inventory[item]['name']] = parsed_item
            else:
                pass

        WsWrap.ws_send(self.client, send_kwargs, jinventory)

    def update_player_health(self):

        send_kwargs = {'type': 'vitals', 'spacing': False}

        if self.vitals['hp_current'] < 0:
            self.vitals['hp_current'] = 0
        
        # update health
        WsWrap.ws_send(self.client, send_kwargs, {'hp_current': self.vitals['hp_current'], "hp_max": self.vitals['hp_max']})

    def update_player_attributes(self):

        send_kwargs = {'type': 'attr', 'spacing': False}
        
        # update core attributes
        WsWrap.ws_send(self.client, send_kwargs, self.core_attributes)

    def update_player_object(self):
       
        # update player object in memory
        players[self.uuid_id].vitals = self.vitals
        players[self.uuid_id].inventory = self.inventory
        players[self.uuid_id].core_attributes = self.core_attributes
        players[self.uuid_id].conditions = self.conditions
        players[self.uuid_id].stow_loc = self.stow_loc
        players[self.uuid_id].location = self.location

    def update_central_db(self):

        send_kwargs = {'type': 'wiki', 'spacing': False}
       
        # update player object in memory
        # central_db = {}

        # for i in global_command_list:
        #     central_db[i] = {'cmd_title': global_command_list[i]['cmd_title'], 
        #                      'cmd_usage': global_command_list[i]['cmd_usage'], 
        #                      'desc': global_command_list[i]['desc']}
        final_list = sorted(global_command_list, key=lambda d: d['cmd_title'])

        WsWrap.ws_send(self.client, send_kwargs, final_list)

    def update_suit_shield(self):

        send_kwargs = {'type': 'suit_shield', 'spacing': False}

        # try:
        if self.inventory['suit']['contents'] == None:
            WsWrap.ws_send(self.client, send_kwargs, {"shield_current": 0, "shield_max": 0})

        if self.inventory['suit']['contents']:
            shield_current = items[self.inventory['suit']['contents'].uuid_id].vitals['shield_current']
            shield_max = items[self.inventory['suit']['contents'].uuid_id].vitals['shield_max_current']
            
            print("Updating:", self.name, "Suit Shield:", {"shield_current": shield_current, "shield_max": shield_max})
            
            WsWrap.ws_send(self.client, send_kwargs, {"shield_current": shield_current, "shield_max": shield_max})

        # except:

        #     print("ERROR Updating Suit Shield for:", self.name)
        #     print("")