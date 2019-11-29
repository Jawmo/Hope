from engine.global_config import *
from engine.gen import Gen
from websocket_server.wswrap import WsWrap

### Lex(icon) Class for language based functions ###

class Lex():
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def pub_print(self, first_person, target_person, third_person, target, send_kwargs):

        # parse words for color changes
        
        first_edit = first_person.split()
        target_edit = target_person.split()
        third_edit = third_person.split()

        try:
            
            for location, word in enumerate(first_edit):
                if self.entity_type['base'] == 'player':
                    
                    if word == self.name:
                        first_edit[location] = "|player|{}|playerx|".format(word.capitalize())
                    
                    if target:
                        if target.entity_type['base'] != "npc":
                            pass
                        else:
                            if word == target.name:
                                first_edit[location] = "|npc|{}|npcx|".format(word)


            for location, word in enumerate(target_edit):

                if word == target.name:
                    target_edit[location] = "|player|{}|playerx|".format(word.capitalize())
                
                if target:
                    if word == self.name:
                        target_edit[location] = "|npc|{}|npcx|".format(word)


            for location, word in enumerate(third_edit):

                if self.entity_type['base'] == 'player':
                    
                    if word == self.name:
                        third_edit[location] = "|player|{}|playerx|".format(word.capitalize())
                    
                    if target:
                        if word == target.name:
                            third_edit[location] = "|npc|{}|npcx|".format(word)


        except AttributeError as error:
            print("LOG | ERROR | PubPrint. Please contact your Admin.", error)

        
        # apply first letter capitalization to first/target/third person output

        # print("LEX:", first_edit)
        if first_edit:
            if "|" in first_edit[:1]:
                first_edit[1] = first_edit[1].capitalize()
            else:
                first_edit[0] = first_edit[0].capitalize()

        first_person = first_edit

        # print("LEX:", target_edit)

        if target_edit:
            if "|" in target_edit[:1]:
                target_edit[1] = target_edit[1].capitalize()
            else:
                target_edit[0] = target_edit[0].capitalize()

        target_person = target_edit

        # print("LEX:", third_edit)
        if third_edit:
            if "|" in third_edit[:1]:
                third_edit[1] = third_edit[1].capitalize()
            else:
                third_edit[0] = third_edit[0].capitalize()

        third_person = third_edit

        
        # print words to client

        if self.entity_type['base'] == "npc":
            if target is not None and target is not self:
                WsWrap.ws_send(target.client, send_kwargs, "{}".format(" ".join(target_person)))

        elif self.entity_type['base'] == "player":
            if first_person == "" or first_person == []:
                pass
            else:
                WsWrap.ws_send(self.client, send_kwargs, "{}".format(" ".join(first_person)))

        if Gen.players_in_room(self):

            for i in Gen.players_in_room(self):

                if i == target:
                    pass
                else:
                    if third_person == "" or third_person == []:
                        pass
                    else:
                        WsWrap.ws_send(i.client, send_kwargs, "{}".format(" ".join(third_person)))

    def comms(self, first_person, target_person, third_person, target, send_kwargs):

        if first_person == "":
            pass
        else:
            WsWrap.ws_send(self.client, send_kwargs, first_person)
            # WsWrap.ws_send(self.client, send_kwargs, "")

        if Gen.players_in_room(self):
            for i in Gen.players_in_room(self):
                if target == None:
                    WsWrap.ws_send(i.client, send_kwargs, third_person)
                    WsWrap.ws_send(i.client, send_kwargs, "")
                else:
                    if target.name == i.name:
                        WsWrap.ws_send(target.client, send_kwargs, target_person)
                        WsWrap.ws_send(target.client, send_kwargs, "")
                    else:
                        WsWrap.ws_send(i.client, send_kwargs, third_person)
                        WsWrap.ws_send(i.client, send_kwargs, "")

    def pub_print_outside(target_room, msg):
        
        for player in target_room.player_inv:

            all_schedules[self.uuid_id]['sched'].eventabs(
                time.time() + 1,                    # event timer
                1,                                  # priority (1 = highest)
                "print_outside",                    # event name
                "print",                            # event type
                Lex.pub_print,                      # action
                kwargs={'msg': msg})                # kwargs 

    def pub_print_ext(self, first_person, target_person, third_person, target, send_kwargs):
        
        for player in room_of_ship.player_inv:
            print(player)
            s.enterabs(time.time() + 1, 1, WsWrap.ws_send, 
                       kwargs={'client': player.client, 'msg': 'A shuttle door opens with a *whoosh*.'})

    def first_three(target):
        
        if len(target) >= 3:
            target_three = target[0] + target[1] + target[2]
        else:
            target_three = target[:1]

        return target_three

    def gender(self, gen_param):
        
        own = "own"
        desc = "desc"
        pro = "pro"

        if self.gender == "male":
            if gen_param == own:
                result = "his"
            elif gen_param == desc:
                result = "him"
            elif gen_param == pro:
                result = "he"
        
        elif self.gender == "female":
            if gen_param == own:
                result = "her"
            elif gen_param == desc:
                result = "her"
            elif gen_param == pro:
                result = "she"

        elif self.gender == "neutral":
            if gen_param == own:
                result = "its"
            elif gen_param == desc:
                result = "its"
            elif gen_param == pro:
                result = "it"

        return result

    def a_an(self):

        if self[0].lower() in ["a", "e", "i", "o", "u", "8"]:
            self = "an " + self
        elif self[0].lower() == "s":
            if len(self) > 1:
                self = "a " + self
            else:
                self = "an " + self
        else:
            self = "a " + self

        return self

    def converted_contents(self):

        contents = self
        converted_contents = []
        for i in contents:
            if len(contents) == 1:
                i = Lex.a_an(i)
            elif i == contents[-1]:
                i = "and " + Lex.a_an(i)
            else:
                i = Lex.a_an(i)
            converted_contents.append(i)

        return converted_contents

    def smile(self, user_input, target):
        # name = "smile"
        # description = "Smile verb.",

        # if you do not target a person or object
        if type(target) == dict:
            Lex.pub_print(
                self=self,
                target=target,
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = "You smile.",
                target_person = "{} smiles.".format(self.name),
                third_person = "{} smiles.".format(self.name))
        
        else:
            # if you target yourself
            if target == self:
                Lex.pub_print(
                    self=self,
                    target=target,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "You smile to yourself.",
                    target_person = "{} smiles to themself.".format(self.name),
                    third_person = "{} smiles to themself.".format(self.name))
            
            # if you target someone else
            else:
                # if target not in Room.players_in_room(self):
                #     Lex.pub_print(
                #         self=self,
                #         target=target,
                #         first_person = "You smile at {}.".format(Lex.a_an(target.name)),
                #         target_person = "",
                #         third_person = "{} smiles at {}.".format(self.name, Lex.a_an(target.name)))
                # else:
                Lex.pub_print(
                    self=self,
                    target=target,
                    send_kwargs={'type': 'text', 'spacing': 1},
                    first_person = "You smile at {}.".format(target.name),
                    target_person = "{} smiles at you.".format(self.name),
                    third_person = "{} smiles at {}.".format(self.name, target.name))