import uuid, copy, json, re
from engine.global_config import *
from engine.db_commands import *
from websocket_server.wswrap import WsWrap
from engine.update_client import Update_Client

from engine.player import Player
from engine.room import Room
from engine.inventory import inv
from engine.sched_mgr.sched_mgr import Sched_Child
from engine.lex import Lex

def check_user(client, server, message):

    # print(message)

    send_kwargs = {'type': 'text', 'spacing': 1}

    if "username" in message:

      user_info = json.loads(message.lower())
      client['uuid_id'] = user_info['username']
      # print("LOG | CHECK USER MSG |", user_info)

    login = check_login(client['uuid_id'])
      
    if login == False:

      if client['type'] == "guest":

          print(client['guest_progress'])

          if client['guest_progress'] == 'name_input':
              
              WsWrap.ws_send(client, send_kwargs, "|comp|Welcome! Three questions and you're in the game.|/comp|")
              WsWrap.ws_send(client, send_kwargs, "|w|1. What is your first name?|/w|")
              client['guest_progress'] = 'name_confirm'

          elif client['guest_progress'] == 'name_confirm':
              
              client['name'] = re.sub("[^a-zA-Z]+", "", message)
              for i in players:
                
                if message.capitalize() == i.capitalize():
                  WsWrap.ws_send(client, send_kwargs, '|w| {} is taken. Please choose another. |/w|'.format(client['name'].capitalize()))    
                  break
              
              else:

                WsWrap.ws_send(client, send_kwargs, '|w|2. {}, is this correct? (y/n)|/w|'.format(client['name'].capitalize()))
                client['guest_progress'] = 'name_confirm2'
              
          elif client['guest_progress'] == 'name_confirm2':
              
              if message == "no" or message == "n":
                  WsWrap.ws_send(client, send_kwargs, "|w|Alright, let's try this again. What is your first name?|/w|")
                  client['guest_progress'] = 'name_confirm'
              elif message == "yes" or message == "y":
                  WsWrap.ws_send(client, send_kwargs, '|w|3. Great. Are you (m)ale or (f)emale?|/w|')
                  client['guest_progress'] = 'gender_input'

          elif client['guest_progress'] == 'gender_input':
              
              if message == "male" or message == "m":
                  gender = "male"

              elif message == "female" or message == "f":
                gender = "female"

              if message != "female" and message != "f" and message != "male" and message != "m":

                WsWrap.ws_send(client, send_kwargs, '|w|Please choose (m)ale or (f)emale.|/w|')
              else:

                WsWrap.ws_send(client, send_kwargs, '|comp|Please stand by. Creating your character...|/comp|')

                client['type'] = 'member_authenticated'
                client['reg'] == "online"

                inventory = copy.deepcopy(inv)
                print("Guest:", client)

                hero = Player(**{
                    "uuid_id": client['uuid_id'],
                    "entity_type": {"base": "player", "group": "registered", "model": None, "sub_model": None},
                    "name": client['name'], 
                    "race": "human",
                    "gender": gender, 
                    "vitals": {"hp_max": 100, "hp_current": 100, "hp_mod": 0, "hp_regen": 1, "hp_regen_mod": 0, "alive": True},
                    "core_attributes": {"title": "Ensign", "str": {"base": 8, "mod": 0}, "dex": {"base": 10, "mod": 0}, "con": {"base": 8, "mod": 0}, "ins": {"base": 12, "mod": 0}, "edu": {"base": 10, "mod": 0}, "soc": {"base": 10, "mod": 0}, "xp": {"current": 0, "buffer": 0, "absorp_rate_percent": 1}}, 
                    "conditions": {"stance": "stand", "action": "None", "state": "awake", "round_time": 0, "help": "enabled", "echo": False},
                    "credit": {"credit": 100},
                    "location": "65d56cbe-f276-4055-899c-3244c0c92003",
                    "player_state": "logged_in",
                    "stow_loc": None, 
                    "client": client,
                    "unique_id": None
                    })

                update_user_player(hero)

                add_new_player_to_db(hero)
                    
                client['obj'] = hero

                # for i in all_schedules:
                #   print(i)

                Sched_Child.create_new_sched(client['obj'])
                

                # update the client
                client['type'] == 'member_authenticated'


                # update the player object in the player list
                players[hero.uuid_id] = hero
                players[client['obj'].uuid_id].player_state = "online"

                WsWrap.ws_send_to_all(send_kwargs, "** A new player, {}, just joined the server.".format(hero.name))
                WsWrap.ws_send(hero.client, send_kwargs, "|comp| Welcome, {}. We've been awaiting your arrival. |compx|".format(hero.name.capitalize()))
                
                WsWrap.ws_send(hero.client, {'type': 'text', 'spacing': 0}, '|success| For your convenience, help cues are currently {}. Help cues will provide additional context or syntax when you type a command. Some commands may not have help associated with them yet. We are working on this. |successx|'.format(client['obj'].conditions['help'].upper()))
                WsWrap.ws_send(hero.client, {'type': 'text', 'spacing': 1}, '|success| Type HELP ON or HELP OFF to toggle this feature. |successx|')

                rooms[hero.location].player_inv.append(client['obj'])
                rooms[hero.location].display_room(hero)

                # update player settings to the client
                Update_Client.update_char_info(client['obj'])
                Update_Client.update_user_settings(client['obj'])
                Update_Client.update_player_health(client['obj'])
                Update_Client.update_player_attributes(client['obj'])
                Update_Client.update_player_list(client['obj'])
                Update_Client.update_player_inventory(client['obj'])
                Update_Client.update_central_db(client['obj'])


    else:
        
        # login = check_login(client['uuid_id'])
        
        inventory = copy.deepcopy(inv)

        hero = players[login]
        hero.inventory = inventory

        client['obj'] = hero
        client['type'] = "member_authenticated"
        players[client['obj'].uuid_id].player_state = "online"

        rooms[hero.location].player_inv.append(client['obj'])

        print("New Client Connected:", client, client['obj'])
        print("")
        client['id'] = client['obj'].unique_id
        print("Updated Client:", client, client['obj'])
        print("")

        if hero.uuid_id in all_schedules:
          pass
        else:
          Sched_Child.create_new_sched(client['obj'])

        for u in items:
            if items[u].location == client['obj'].uuid_id:
                if "location" in items[u].location_body:
                    # print("LOG: Re-adding item", items[u].name, "to", items[u].location_body['location'])
                    hero.inventory[items[u].location_body['location']]['contents'] = items[u]

        # # check round_time
        # if hero.conditions['round_time'] > 0:
        #   if 'round_time' in all_schedules[hero.uuid_id]['sched'].event_names:
        #     hero.round_time_dec()
        

        # update the player object in the player list
        
        client['obj'].client = client

        Lex.pub_print(
          self=client['obj'],
          target=None,
          send_kwargs={'type': 'text', 'spacing': 1},
          first_person = "|comp| Welcome back, {}. We've been awaiting your arrival. |compx|".format(hero.name.capitalize()),
          target_person = "",
          third_person = "{} just arrived.".format(client['obj'].name.capitalize()))

        WsWrap.ws_send(hero.client, {'type': 'text', 'spacing': 0}, '|success| For your convenience, help cues are currently |successx| |y| {}|yx|. |success| Help cues will provide additional context or syntax when you type a command. Some commands may not have help associated with them yet. We are working on this. |successx|'.format(client['obj'].conditions['help'].upper()))
        WsWrap.ws_send(hero.client, {'type': 'text', 'spacing': 1}, '|success| Type HELP ON or HELP OFF to toggle this feature. |successx|')

        WsWrap.ws_send(hero.client, {'type': 'text', 'spacing': 1}, '|success| You may also toggle the input echo on/off by typing "echo". Default is off. |successx|')


        rooms[client['obj'].location].display_room(client['obj'])

        # update player settings to the client
        Update_Client.update_char_info(client['obj'])
        Update_Client.update_user_settings(client['obj'])
        Update_Client.update_player_health(client['obj'])
        Update_Client.update_suit_shield(client['obj'])
        Update_Client.update_player_attributes(client['obj'])
        Update_Client.update_player_list(client['obj'])
        Update_Client.update_player_inventory(client['obj'])
        Update_Client.update_central_db(client['obj'])
