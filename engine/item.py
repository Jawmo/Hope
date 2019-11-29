import uuid

from engine.global_config import *
from engine.db_commands import *
from engine.update_client import Update_Client

from engine.lex import *

from engine.join_tables.join_table_items import *
from engine.suits.suit_templates import alpha_suit_table

###### Item Class ######

class Item():
    def __init__(self, **kwargs):

        self.uuid_id =          kwargs['uuid_id']
        self.join_table =       kwargs['join_table']
        self.entity_type =      item_table[kwargs['join_table']['keyword']]['entity_type']
        self.name =             kwargs['description']['name']
        self.description =      kwargs['description']['desc']
        self.keyword =          kwargs['keyword']
        self.size =             item_table[kwargs['join_table']['keyword']]['size']
        self.weight =           item_table[kwargs['join_table']['keyword']]['weight']
        self.capacity =         item_table[kwargs['join_table']['keyword']]['capacity']
        self.worn =             item_table[kwargs['join_table']['keyword']]['worn']
        self.attributes =       kwargs['attributes']
        self.dynamic_stats =    kwargs['dynamic_stats']
        self.static_stats =     item_table[kwargs['join_table']['keyword']]['static_stats']
        self.room_target =      kwargs['room_target']
        self.combines_with =    item_table[kwargs['join_table']['keyword']]['combines_with']
        self.item_inv =         []
        self.location =         kwargs['location']
        self.location_body =    kwargs['location_body']
        self.owner =            kwargs['owner']
        self.is_open =          kwargs['is_open']
        self.vitals =           kwargs['vitals']

    def convert_entry_to_obj(self):

        # print("CONVERTING item:", items[self], "|", items[self][0]['keyword'])

        new_item = Item(self,                                               # uuid
                    item_table[items[self][0]['keyword']]['entity_type'],   # entity_type
                    items[self][2],                                         # keyword
                    items[self][3],                                         # description
                    item_table[items[self][0]['keyword']]['size'],          # size
                    item_table[items[self][0]['keyword']]['weight'],        # weight
                    item_table[items[self][0]['keyword']]['capacity'],      # capacity
                    item_table[items[self][0]['keyword']]['worn'],          # worn
                    items[self][4],                                         # attributes
                    items[self][5],                                         # dynamic_stats
                    item_table[items[self][0]['keyword']]['static_stats'],  # static_stats
                    items[self][6],                                         # room_target
                    item_table[items[self][0]['keyword']]['combines_with'], # combines_with
                    items[self][7],                                         # is_open
                    [],                                                     # item_inv
                    items[self][8],                                         # location
                    items[self][9],                                         # location_body
                    item_table[items[self][0]['keyword']]['vitals'],        # vitals
                    items[self][11])                                        # owner


        items[self] = new_item
        print("CONVERT ITEM TO OBJ | FINISHED:", new_item.name, new_item, new_item.location)

    def entity_description(self, user, user_input, input_kwargs):
        
        if "wall_display" in self.attributes:
        
            if self.item_inv != []:

                first_person_value = "{} On it, you see {}.".format(self.description, ", ".join(self.item_inv))
                target_person_value = ""
                third_person_value = "{} observes {}.".format(user.name, Lex.a_an(input_kwargs['target'].name))

            else:

                first_person_value = "{}".format(self.description)
                target_person_value = ""
                third_person_value = "{} observes {}.".format(user.name, Lex.a_an(self.name))

        else:

            if not self.description:
                
                first_person_value = "It looks pretty generic."
                target_person_value = ""
                third_person_value = ""
            
            else:

                first_person_value = "{}".format(self.description)
                target_person_value = ""
                third_person_value = "{} observes {}.".format(user.name, Lex.a_an(self.name))

        Lex.pub_print(
            self=user,
            target=input_kwargs['target'],
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = first_person_value,
            target_person = target_person_value,
            third_person = third_person_value,
            )


    def items_in_item(self, user_input, input_kwargs):

        print("I in I:", input_kwargs)
        if "is_container" not in input_kwargs['target'].attributes:
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "This has no storage.")
        else:

            items_in = []
            for i in input_kwargs['target'].item_inv:
                items_in.append(i.name)
                
            if items_in == []:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You see nothing.")
            else:
                WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You see {}.".format(", ".join(Lex.converted_contents(items_in))))
  
    
    def open_close(self, user_input, input_kwargs):

        if user_input[0] == "open":
            input_kwargs['target'].is_open = True

            Lex.pub_print(
                self=self,
                target=input_kwargs['target'],
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You open {}.".format(Lex.a_an(input_kwargs['target'].name)),
                target_person = "",
                third_person = "{} opens {}.".format(self.name, Lex.a_an(input_kwargs['target'].name)))

        elif user_input[0] == "close":
            input_kwargs['target'].is_open = False

            Lex.pub_print(
                self=self,
                target=input_kwargs['target'],
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You close {}.".format(Lex.a_an(input_kwargs['target'].name)),
                target_person = "",
                third_person = "{} closes {}.".format(self.name, Lex.a_an(input_kwargs['target'].name)))

        Update_Client.update_player_inventory(self)


    def action_pull(self, user_input, input_kwargs):

        if input_kwargs['target'].entity_type['group'] == "armor":
            
            input_kwargs['target'].action_pull(user_input, input_kwargs)
        
        else:
        
            WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You pull it.")