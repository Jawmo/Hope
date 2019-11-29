import sched, time, random, copy
from pprint import pprint
from engine.global_lists import *
# from engine.global_config import *
from engine.lex import Lex
from engine.gen import Gen
from engine.character import Character
from engine.inventory import inv
from engine.sched_mgr.sched_mgr import Sched_Child
from engine.combat.combat_main import Combat

from engine.join_tables.join_table_npcs import npc_table
from engine.npcs.npc_combat_table import npc_combat_table, hit_table

###### Item Class ######

class Npc(Character):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.entity_type =      npc_table[kwargs['join_table']]['entity_type']
        self.race =             npc_table[kwargs['join_table']]['description']['race']
        self.core_attributes =  npc_table[kwargs['join_table']]['core_attributes']
        self.join_table =       kwargs['join_table']
        self.description =      npc_table[kwargs['join_table']]['description']
        self.npc_state =        kwargs['npc_state']
        self.supply =           kwargs['supply']
        self.demand =           kwargs['demand']
        self.home_loc =         npc_table[kwargs['join_table']]['home_loc']
        self.demeanor =         kwargs['demeanor']

        Sched_Child.create_new_sched(self)

    def npc_assess(self, **npc_kwargs):

        # alert types:
        # sleep = not performing any tasks
        # awake = moving rooms, searching for targets
        # engaged = engaging a target in combat
            
        if self.conditions['state'] == "sleep":
            pass

        elif self.conditions['state'] != "sleep":

            players_in_room = Gen.players_in_room(self)
            
            if players_in_room == []:
                
                exit = Gen.random_movement(self)

                if exit == None:
                    pass
                else:
                    rand_die = random.randint(1, 1)

                    Character.navigate(self, None, exit)
                    all_schedules[self.uuid_id]['sched'].eventabs(time.time() + rand_die, 1, "npc_assess", "npc", Npc.npc_assess, kwargs={"self": self})

            elif players_in_room != []:

                input_kwargs = {}
                input_kwargs['target'] = random.choice(players_in_room)

                if input_kwargs['target'].vitals['alive'] == False:
                    
                    Lex.pub_print(
                        self=self,
                        target=input_kwargs['target'],
                        send_kwargs={'type': 'text', 'spacing': 1},
                        first_person = "",
                        target_person = f"{Lex.a_an(self.name).capitalize()} smirks at your dead body.",
                        third_person = f"{Lex.a_an(self.name).capitalize()} smirks at {input_kwargs['target'].name}'s dead body.")

                    self.conditions['state'] = "awake"
                    print(f"NPC ASSESS | Entity: {self.name} changing state to: {self.conditions['state']}.")

                else:
                    self.conditions['state'] = "engaged"
                    print(f"NPC ASSESS | Entity: {self.name} changing state to: {self.conditions['state']}.")
                    print("")

                    roll = Gen.random_number(2, 1, 6)
                    combat_choice = Gen.random_number(1, 1, 6)

                    Combat.attack(self, None, input_kwargs)


    def convert_npcs_to_obj():

        inventory = copy.deepcopy(inv)

        for i in npcs:
            print(i, npcs[i])
            # npc_sched = sched.scheduler(time.time, time.sleep)

            npc_obj = Npc(i,                                            # uuid
                            npc_table[npcs[i][6]]['entity_type'],         # entity_type
                            npcs[i][6],                                 # join_table
                            npcs[i][0],                                 # name
                            npc_table[npcs[i][6]]['race'],              # race
                            npcs[i][1],                                 # gender
                            npcs[i][2],                                 # vitals
                            npc_table[npcs[i][6]]['core_attributes'],   # core_attributes
                            npcs[i][3],                                 # conditions
                            npcs[i][4],                                 # credit
                            inventory,                                        # inventory
                            npcs[i][5],                                 # location
                            npcs[i][7],                                 # npc_desc
                            npcs[i][8],                                 # npc_state
                            npcs[i][9],                                 # supply
                            npcs[i][10],                                # demand
                            npc_table[npcs[i][6]]['home_loc'],          # hom_loc
                            npcs[i][11])                                # demeanor


            # print(npc_sched)
            Sched_Child.create_new_sched(npc_obj)
            Npc.npc_assess(npc_obj)

            npcs[i] = npc_obj

            # pprint(vars(npc_obj))

    def display_npc_inventory(target):

        npc_inv = []

        for i in target.inventory:
            if target.inventory[i]['contents'] == None:
                pass
            else:
                npc_inv.append("{} {} {} {}".format(target.inventory[i]['contents'].name, 
                                                target.inventory[i]['worn'], 
                                                Lex.gender(target, "own"), 
                                                target.inventory[i]['name']))
        if npc_inv == []:
            npc_inv = "nothing"

        print(npc_inv)
        return npc_inv