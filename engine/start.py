from engine.global_config import *
from engine.global_lists import *
from engine.db_commands import *
from engine.player import Player
from engine.npc import Npc
from engine.room import Room

from engine.command_list import all_commands, load_global_command_list
from engine.loops.main_loop import MainLoop

from engine.item import Item
from engine.items.gun import Gun
from engine.items.guns.pistol import Pistol
from engine.items.guns.pistol_9mm import Pistol_9mm
from engine.items.guns.assault_rifle import Assault_Rifle
from engine.items.guns.assault_rifle_energy import Assault_Rifle_Energy
from engine.ship.ship_main import Ship
from engine.suits.suit import TacSuit

from importlib import import_module

from pprint import pprint

##### Pregame Initialization #####

def start():
    
    # load global command list
    load_global_command_list()
    # print(global_command_list)


    #load players
    print("Loading players...")
    load_all_players(players)
    print("Converting players to objects...")
    for player in players:
        players[player] = Player(**players[player])
        
    # for i in players:
    #     print(i, pprint(vars(players[i])))
    

    # load rooms
    print("")
    print("Loading rooms...")
    load_all_rooms(rooms)
    print("Converting rooms to objects...")
    for room in rooms:
        rooms[room] = Room(**rooms[room])
    # for i in rooms:
    #     pprint(vars(rooms[i]))


    # load items
    print("")
    print("Loading items...")
    load_all_items(items)
    print("Converting items to objects...")
    
    class_dict = {
        "Item": Item,
        "TacSuit": TacSuit,
        "Ship": Ship,
        "Gun": Gun,
        "Pistol": Pistol,
        "Pistol_9mm": Pistol_9mm,
        "Assault_Rifle": Assault_Rifle,
        "Assault_Rifle_Energy": Assault_Rifle_Energy
    }
    
    for i in items:
        instance_class = class_dict[items[i]['join_table']['class']]
        items[i] = instance_class(**items[i])


    # load npcs
    print("")
    print("Loading npcs...")
    load_all_npcs(npcs)
    # print("items before:", items)
    print("Converting npcs to objects...")
    for npc in npcs:
        npcs[npc] = Npc(**npcs[npc])
    

    print("")
    print("Putting items in rooms and other items...")
    if items:

        print("Items...")
        for i in items:
            # pprint(items[i])
            for x in items:
                # pprint(vars(items[x]))
                if items[i].location == items[x].uuid_id:
                    print(" Putting item:", items[i].name, "in item:", items[items[i].location].name)
                    items[items[i].location].item_inv.append(items[i])

        print("Rooms...")
        for i in items:
            # pprint(vars(items[i]))
            for y in rooms:
                if items[i].location == rooms[y].uuid_id:
                    print(" Putting item:", items[i].name, "in room:", rooms[items[i].location].name)
                    rooms[items[i].location].item_inv.append(items[i])

        print("Players...")
        for i in items:
            for z in players:
                if items[i].location == players[z].uuid_id:
                    print(" Putting item:", items[i].name, "in player:", players[items[i].location].name)
                    # print(players[z])
                    # print(items[i])
                    players[z].inventory[items[i].location_body['location']]['contents'] = items[i]

        print("NPCs...")
        for i in items:
            for a in npcs:
                if items[i].location == npcs[a].uuid_id:
                    print(" Putting item:", items[i].name, "in npc:", npcs[items[i].location].name)
                    npcs[a].inventory['r_hand']['contents'] = items[i]

    if npcs:
        print("Adding NPCs to rooms...")
        for i in npcs:
            # pprint(vars(npcs[i]))
            for a in rooms:
                if npcs[i].location == rooms[a].uuid_id:
                    print(" Putting npc:", npcs[i].name, "in room:", rooms[npcs[i].location].name)
                    rooms[a].npc_inv.append(npcs[i])
    
    print("Done.")

    MainLoop.main_loop_all()
