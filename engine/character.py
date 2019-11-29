import copy

from engine.global_config import *

from pprint import pprint
from engine.update_client import Update_Client
from engine.handler.input_handler import Input_Handler
from engine.status_check import Status_Check

from websocket_server.wswrap import WsWrap

from engine.lex import Lex
from engine.gen import Gen
from engine.inventory import inv
from engine.room import Room
from engine.ship.ship_main import Ship
from engine.holodeck.holodeck import Holodeck
from engine.special.item_animations import Item_Animations

class Character():
    def __init__(self, **kwargs):

        inventory = copy.deepcopy(inv)
        # print(kwargs['description']['race'])

        self.uuid_id =         kwargs['uuid_id']
        self.entity_type =     None
        self.name =            kwargs['description']['name']
        self.race =            kwargs['description']['race']
        self.gender =          kwargs['description']['gender']
        self.description =     kwargs['description']['desc']
        self.vitals =          kwargs['vitals']
        self.core_attributes = None
        self.conditions =      kwargs['conditions']
        self.credit =          kwargs['credit']
        self.inventory =       inventory
        self.location =        kwargs['location']

    def say(self, user_input, input_kwargs):

        print("SAY | User Input:", user_input)

        if len(user_input) < 2:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "|alert| Syntax: |alertx| '(sentence) or SAY (sentence).")
        else:
            if self.entity_type['base'] == 'npc':
                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = '|npc| You say|npcx|, "{}"'.format(" ".join(user_input[1:])),
                    target_person = "",
                    third_person = '|npc| {} says|npcx|, "{}"'.format(self.name.capitalize(), " ".join(user_input[1:])))
            else:

                if user_input[1] == "computer,":
                    send_kwargs = {'type': 'text', 'spacing': 1}
                else:
                    send_kwargs = {'type': 'text', 'spacing': 1}

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs=send_kwargs,
                    first_person = '|self_speech| You say|self_speechx|, "{}"'.format(" ".join(user_input[1:])),
                    target_person = "",
                    third_person = '|player_speech| {} says|player_speechx|, "{}"'.format(self.name.capitalize(), " ".join(user_input[1:])))
           
            
                if user_input[1] == "computer,":
                    self.voice_command(user_input, input_kwargs)


    def comms(self, user_input, input_kwargs):

        Lex.pub_print(
            self=self,
            target=None,
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = '|self_comm|You say|/self_speech|, "{}"'.format(" ".join(user_input)),
            target_person = "",
            third_person = '|player_comm|{} says|/player_speech|, "{}"'.format(self.name.capitalize(), " ".join(user_input)))


    def entity_description(self, user, user_input, input_kwargs):

        if self.vitals['alive'] == True:

            first_person_value = "{}".format(self.description['desc'])
            target_person_value = ""
            third_person_value = "{} observes {}.".format(self.description['name'], Lex.a_an(self.description['name']))

        else:

            first_person_value = "{} is dead. {}".format(Lex.gender(self.description['name'], "pro").capitalize(), self.description['desc']),               
            target_person_value = "{} observes your dead body.".format(self.description['name'])
            third_person_value = "{} observes {}.".format(self.description['name'], Lex.a_an(self.description['name']))

        Lex.pub_print(
            self=user,
            target=input_kwargs['target'],
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = first_person_value,
            target_person = target_person_value,
            third_person = third_person_value,
            )

    def round_time_set(self, round_time):

        if self.conditions['round_time'] != 0:
            pass
        else:
            self.conditions['round_time'] = round_time
            self.conditions['init_round_time'] = round_time
            Update_Client.update_init_round_time(self)
            
            all_schedules[self.uuid_id]['sched'].eventabs(
                time.time() + 1,                    # event timer
                1,                                  # priority (1 = highest)
                "round_time_dec",                   # event name
                "round_time",                       # event type
                Character.round_time_dec,           # action
                kwargs={"self": self})              # kwargs 


    def round_time_dec(self):
        
        if self.conditions['round_time'] < 1:
            
            # pass
            all_schedules[self.uuid_id]['sched'].remove_event_name("round_time_dec", "rt")

        else:
            
            self.conditions['round_time'] = self.conditions['round_time'] - 1
            print("RT DEC | Reducing RT from", self.conditions['round_time'], "to", self.conditions['round_time'] - 1)

            all_schedules[self.uuid_id]['sched'].eventabs(
                time.time() + 1,                    # event timer
                1,                                  # priority (1 = highest)
                "round_time_dec",                   # event name
                "rt",                               # event type
                Character.round_time_dec,           # action
                kwargs={"self": self})              # kwargs

        Update_Client.update_round_time(self)


    def change_stance(self, user_input, input_kwargs):

        # function

        if self.conditions['stance'] == user_input[0]:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You are already doing that.")
        else:

            if user_input[0] == "stand":
                
                self.conditions['stance'] = "stand"

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = 'You stand back up.',
                    target_person = "",
                    third_person = '{} stands up.'.format(self.name.capitalize()))

            elif user_input[0] == "sit":

                self.conditions['stance'] = "sit"

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = 'You sit down.',
                    target_person = "",
                    third_person = '{} sits down.'.format(self.name.capitalize()))
            
            elif user_input[0] == "lie":

                self.conditions['stance'] = "lie"

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = 'You lie down.',
                    target_person = "",
                    third_person = '{} lies down.'.format(self.name.capitalize()))

    def check_death(self, user_input, input_kwargs):

        if input_kwargs['target'].vitals['hp_current'] <= 0:

            if input_kwargs['target'].entity_type['base'] == "npc":

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "|npc|{} crumples into a heap and dies.|npcx|".format(Lex.a_an(input_kwargs['target'].name).capitalize()),
                    target_person = "",
                    third_person = "|npc|{} crumples into a heap and dies.|npcx|".format(Lex.a_an(input_kwargs['target'].name).capitalize()))
            
                input_kwargs['target'].conditions['stance'] = "lying"
                input_kwargs['target'].conditions['state'] = "sleep"
                input_kwargs['target'].vitals['alive'] = False
                
                # clear the event schedule
                ent_sched = all_schedules[input_kwargs['target'].uuid_id]['sched']
                list(map(ent_sched.cancel, ent_sched.queue))

            elif input_kwargs['target'].entity_type['base'] == "player":
            
                input_kwargs['target'].conditions['stance'] = "lying"
                input_kwargs['target'].vitals['alive'] = False

                Lex.pub_print(
                    self=self,
                    target=input_kwargs['target'],
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "",
                    target_person = "|alert|You crumple into a heap and die.|alertx|",
                    third_person = "{} crumples into a heap and dies.".format(input_kwargs['target'].name).capitalize())


    def hp_regen(self):
        
        if self.vitals['hp_current'] + self.vitals['hp_regen'] > self.vitals['hp_max']:
            self.vitals['hp_current'] = self.vitals['hp_max']
        else:
            self.vitals['hp_current'] += self.vitals['hp_regen']
        
        Update_Client.update_player_health(self)

        # all_schedules[self.uuid_id]['sched'].eventabs(
        #     time.time() + 1,                    # event timer
        #     1,                                  # priority (1 = highest)
        #     "hp_regen",                         # event name
        #     "vitals",                           # event type
        #     Character.hp_regen,                 # action
        #     kwargs={"self": self})              # kwargs 

    def wear_item(self, user_input, input_kwargs):

        if input_kwargs['target'] == self.inventory['r_hand']['contents']:
            hand = self.inventory['r_hand']
            contents = self.inventory['r_hand']['contents']

        elif input_kwargs['target'] == self.inventory['l_hand']['contents']:
            hand = self.inventory['l_hand']
            contents = self.inventory['l_hand']['contents']

        self.inventory[contents.worn]['contents'] = contents
        self.inventory[contents.worn]['contents'].location = self.uuid_id
        self.inventory[contents.worn]['contents'].location_body['state'] = "worn"
        self.inventory[contents.worn]['contents'].location_body['location'] = contents.worn
        hand['contents'] = None

        Item_Animations.wear_animation(self, user_input, input_kwargs)
        Update_Client.update_player_inventory(self)

        if input_kwargs['target'].entity_type['group'] == 'armor':
            Update_Client.update_suit_shield(self)


    def remove_item(self, user_input, input_kwargs):

        print(self.inventory['suit'])
        for inv in self.inventory:
            if input_kwargs['target'] == self.inventory[inv]['contents']:
                if not self.inventory['r_hand']['contents']:
                    self.inventory['r_hand']['contents'] = input_kwargs['target']
                    self.inventory[inv]['contents'] = None
                    input_kwargs['target'].location_body['state'] = "not_worn"
                    break

                elif not self.inventory['l_hand']['contents']:
                    self.inventory['l_hand']['contents'] = input_kwargs['target']
                    self.inventory[inv]['contents'] = None
                    input_kwargs['target'].location_body['state'] = "not_worn"
                    break
            
        print(self.inventory['suit'])

        Item_Animations.remove_animation(self, user_input, input_kwargs)
        Update_Client.update_player_inventory(self)

        if input_kwargs['target'].entity_type['group'] == 'armor':
            Update_Client.update_suit_shield(self)

    def swap_hands(self, user_input, input_kwargs):
        right_hand = self.inventory['r_hand']['contents']
        left_hand = self.inventory['l_hand']['contents']
    
        self.inventory['r_hand']['contents'] = left_hand
        self.inventory['l_hand']['contents'] = right_hand

        Lex.pub_print(
            self=self,
            target=None,
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = "You swap the items in your hands.",
            target_person = "",
            third_person = "{} swaps the items in {} hands.".format(self.name.capitalize(), Lex.gender(self, "own")))

        Update_Client.update_player_inventory(self)

    def get_item(self, user_input, input_kwargs):

        all_ok = False
        obj_generator = False

        if input_kwargs['target'] in Gen.items_in_room(self):

            print(input_kwargs['target'], input_kwargs['target'].attributes)

            if "obj_generator" in input_kwargs['target'].attributes:
                print("obj_gen")
            else:
                rooms[input_kwargs['target'].location].item_inv.remove(input_kwargs['target'])

            all_ok = True

        elif input_kwargs['target_parent'] is not None:

            container = items[input_kwargs['target_parent'].uuid_id]
            items[input_kwargs['target_parent'].uuid_id].item_inv.remove(input_kwargs['target'])

            all_ok = True

        elif input_kwargs['target'] == self.inventory['r_hand']['contents'] or input_kwargs['target'] == self.inventory['l_hand']['contents']:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You already have that.")

        if all_ok == True:

            if self.inventory['r_hand']['contents'] == None:
                hand = self.inventory['r_hand']
                input_kwargs['target'].location = self.uuid_id
                input_kwargs['target'].location_body['location'] = "r_hand"
                self.inventory['r_hand']['contents'] = input_kwargs['target']
                Update_Client.update_player_inventory(self)

            elif self.inventory['l_hand']['contents'] == None:
                hand = self.inventory['l_hand']
                input_kwargs['target'].location = self.uuid_id
                input_kwargs['target'].location_body['location'] = "l_hand"
                self.inventory['l_hand']['contents'] = input_kwargs['target']
                Update_Client.update_player_inventory(self)

        if input_kwargs['target_parent'] is not None:

            Lex.pub_print(
                self=self,
                target=input_kwargs['target'],
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You pull {} out from inside of {}.".format(Lex.a_an(input_kwargs['target'].name), Lex.a_an(container.name)),
                target_person = "",
                third_person = "{} pulls {} from inside of {}.".format(self.name, Lex.a_an(input_kwargs['target'].name), Lex.a_an(container.name)))

        else:

            Lex.pub_print(
                self=self,
                target=None,
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You pickup {} in your {}.".format(Lex.a_an(input_kwargs['target'].name), hand['name']),
                target_person = "",
                third_person = "{} picks up {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))


    def drop_item(self, user_input, input_kwargs):

        if self.inventory['r_hand']['contents'] == input_kwargs['target']:
            self.inventory['r_hand']['contents'] = None
            input_kwargs['target'].location = self.location
            input_kwargs['target'].location_body['location'] = None
            rooms[self.location].item_inv.append(input_kwargs['target'])

            print("[LOG]: Dropped item:", self.inventory['r_hand']['contents'])

            Lex.pub_print(
                self=self,
                target=input_kwargs['target'],
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You drop {}.".format(Lex.a_an(input_kwargs['target'].name)),
                target_person = "",
                third_person = "{} drops {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

            Update_Client.update_player_inventory(self)

        elif self.inventory['l_hand']['contents'] == input_kwargs['target']:
            self.inventory['l_hand']['contents'] = None
            input_kwargs['target'].location = self.location
            input_kwargs['target'].location_body['location'] = None
            rooms[self.location].item_inv.append(input_kwargs['target'])

            print("[LOG]: Dropped item:", self.inventory['l_hand']['contents'])

            Lex.pub_print(
                self=self,
                target=input_kwargs['target'],
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You drop {}.".format(Lex.a_an(input_kwargs['target'].name)),
                target_person = "",
                third_person = "{} drops {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

            Update_Client.update_player_inventory(self)

        else:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You don't have that.")

    def put_item(self, user_input, input_kwargs):

        if self.inventory['r_hand']['contents'] == input_kwargs['target']:
            hand = self.inventory['r_hand']

        elif self.inventory['l_hand']['contents'] == input_kwargs['target']:
            hand = self.inventory['l_hand']

        input_kwargs['target_parent'].item_inv.append(hand['contents'])
        hand['contents'] = None

        Update_Client.update_player_inventory(self)

        Lex.pub_print(
                self=self,
                target=None,
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You put {} in {}.".format(Lex.a_an(input_kwargs['target'].name), Lex.a_an(input_kwargs['target_parent'].name)),
                target_person = "",
                third_person = "{} puts {} in {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name), Lex.a_an(input_kwargs['target_parent'].name)))

    def navigate(self, user_input, name):

        name = name

        travel_verb_first = "travel"
        travel_verb_third = "travels"

        if name in rooms[self.location].exits:
            exit_room = rooms[self.location].exits[name]

            if self.entity_type['base'] == "npc":
                rooms[self.location].npc_inv.remove(self)
                self.location = exit_room
                rooms[self.location].npc_inv.append(self)

                print("AI |", self.name, "moving rooms.")

                if self.entity_type['group'] != "human":
                    Lex.pub_print(
                        self=self,
                        target=None,
                        send_kwargs={'type': 'text', 'spacing': 1},
                        first_person = "",
                        target_person = "",
                        third_person = "|alert|{} just arrived.|alertx|".format(Lex.a_an(self.name).capitalize()))

                else:
                    Lex.pub_print(
                        self=self,
                        target=None,
                        send_kwargs={'type': 'text', 'spacing': 1},
                        first_person = "",
                        target_person = "",
                        third_person = "|alert|{} just arrived.|alertx|".format(self.name.capitalize()))

            else:
                rooms[self.location].player_inv.remove(self)

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "You {} {}.".format(travel_verb_first, name),
                    target_person = "",
                    third_person = "{} {} {} {}.".format(self.core_attributes['title'], self.name.capitalize(), travel_verb_third, name))

                self.location = exit_room
                rooms[self.location].player_inv.append(self)
                rooms[self.location].display_room(self)

                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "",
                    target_person = "",
                    third_person = "{} {} just arrived.".format(self.core_attributes['title'], self.name.capitalize()))
            

        else:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't go there.")

        rooms[self.location].render_map(self)

    def enter_door(self, user_input, input_kwargs):

        print(input_kwargs)
        if input_kwargs['target'] == None:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Usage: go <door>. For navigation, just use n, s, o, up, down, etc.")
        else:

            if not "is_door" in input_kwargs['target'].attributes:
                Lex.pub_print(
                    self=self,
                    target=input_kwargs['target'],
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "You walk towards {}.".format(Lex.a_an(input_kwargs['target'].name)),
                    target_person = "",
                    third_person = "{} walks towards {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

            elif input_kwargs['target'].is_open == False:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That is closed.")
            
            else:

                Lex.pub_print(
                    self=self,
                    target=input_kwargs['target'],
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "You enter {}.".format(Lex.a_an(input_kwargs['target'].name)),
                    target_person = "",
                    third_person = "{} enters {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

                print(input_kwargs['target'])
                if rooms[input_kwargs['target'].room_target['target']].entity_type['group'] == "holodeck":

                    Holodeck.enter_holo(self, user_input, input_kwargs)

                else:

                    rooms[self.location].player_inv.remove(self)
                    print(self.location)
                    self.location = input_kwargs['target'].room_target['target']
                    print(self.location)
                    rooms[self.location].player_inv.append(self)
                    rooms[self.location].display_room(self)

                    Lex.pub_print(
                        self=self,
                        target=None,
                        send_kwargs={'type': 'text', 'spacing': 1},
                        first_person = "",
                        target_person = "",
                        third_person = "{} just arrived.".format(self.name.capitalize()))

        rooms[self.location].render_map(self)

    def search_target(self, user_input, input_kwargs):

        inv_dropped = []
        
        for i in input_kwargs['target'].inventory:

            inv_item = input_kwargs['target'].inventory[i]['contents']

            if input_kwargs['target'].inventory[i]['contents'] == None:
                pass
            else:
                inv_dropped.append(input_kwargs['target'].inventory[i]['contents'].name)
                inv_item.location = self.location
                input_kwargs['target'].inventory[i]['contents'] = None
                rooms[self.location].item_inv.append(inv_item)

        if inv_dropped == []:

            Lex.pub_print(
            self=self,
            target=None,
            send_kwargs={'type': 'text', 'spacing': 0},
            first_person = "You pat down {} but it had nothing of value.".format(Lex.a_an(input_kwargs['target'].name), ", ".join(inv_dropped)),
            target_person = "",
            third_person = "{} searches {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

        else:

            Lex.pub_print(
                self=self,
                target=None,
                send_kwargs={'type': 'text', 'spacing': 0},
                first_person = "You pat down {} and find {}.".format(Lex.a_an(input_kwargs['target'].name), ", ".join(inv_dropped)),
                target_person = "",
                third_person = "{} searches {}.".format(self.name.capitalize(), Lex.a_an(input_kwargs['target'].name)))

        Lex.pub_print(
            self=self,
            target=None,
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = "The {} decays away.".format(input_kwargs['target'].name),
            target_person = "",
            third_person = "The {} decays away.".format(input_kwargs['target'].name))

        del all_schedules[input_kwargs['target'].uuid_id]
        rooms[self.location].npc_inv.remove(input_kwargs['target'])

    def voice_command(self, user_input, input_kwargs):
        
        if rooms[self.location].entity_type['group'] != "ship_personal":

            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You are not in a ship.")

        else:

            # establish variables
            input_kwargs['ship_id'] = rooms[self.location].ship_id
            input_kwargs['room_of_ship'] = rooms[items[input_kwargs['ship_id']].location]
            input_kwargs['room_ship_list'] = []

            # check if player owns the ship for auth to perform commands
            if rooms[self.location].owner != self.name:
                Lex.pub_print(
                    self=self,
                    target=None,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = f'|comp| "Unauthorized." |compx|',
                    target_person = "",
                    third_person = f'|comp| "Unauthorized." |compx|')

            # if checks pass, go on to find the command and run the associated function
            else:
                # print(user_input)
                rooms[self.location].ship_id.voice_command(self, user, user_input, input_kwargs)