import collections

from engine.global_config import *
from engine.functions import look
from engine.db_commands import update_db_item
from engine.status_check import Status_Check
from engine.lex import Lex
from engine.character import Character
from engine.player import Player
from engine.room import Room
from engine.item import Item
from engine.items.gun import Gun
from engine.skill import Skill
from engine.admin_cmd.admin_cmd import Admin_Cmd
from engine.combat.combat_main import Combat
from engine.db.db_modify import update_all_items, update_player

##### Command List #####

def func_help(self):
    
    for i in all_commands:
        server.send_message(self.client, speech, str((all_commands[i]['name'], all_commands[i]['desc']), all_commands[i]['hotkey']))

def load_global_command_list():

    for i in all_commands:
        global_command_list.append({'cmd_title' : all_commands[i]['cmd_title'],
                                    'cmd_usage' : all_commands[i]['cmd_usage'],
                                    'desc'      : all_commands[i]['desc'],
                                    'hotkey'    : all_commands[i]['hotkey']})


database_commands = {
    
    "updateitem": {
        "name"          :   "updateitem",
        "need_com_name" :   "no",
        "need_com_input":   "no",
        "hotkey"        :   ["updateitem"],
        "requirements"  :   {},
        "func"          :   update_all_items},
        "access_level"  :   "admin",
    
    "updateplayer": {
        "name"          :   "updateplayer",
        "need_com_name" :   "no",
        "need_com_input":   "no",
        "hotkey"        :   ["updateplayer"],
        "requirements"  :   {},
        "func"          :   update_player},
        "access_level"  :   "admin"

}

all_commands = {

    "help": {
        "name"          :   "Help",
        "cmd_title"     :   "Help",
        "cmd_usage"     :   "HELP ON or HELP OFF",
        "desc"          :   "Turn HELP on or off for commands as you use them.",
        "need_com_name" :   "yes",
        "need_com_input":   "yes",
        "hotkey"        :   ["help"],
        "requirements"  :   {},
        "func"          :   Player.help,
        "access_level"  :   "player"},

    "echo": {
        "name"          :   "Echo",
        "cmd_title"     :   "Exho",
        "cmd_usage"     :   "Echo",
        "desc"          :   "Turn your echo on or off. Simply type 'echo' to toggle it on or off.",
        "need_com_name" :   "no",
        "need_com_input":   "no",
        "hotkey"        :   ["echo"],
        "requirements"  :   {},
        "func"          :   Player.echo,
        "access_level"  :   "player"},
    
    # "updateitem": {
    #     "name"          :   "updateitem",
    #     "cmd_title"     :   "Pull Object",
    #     "cmd_usage"     :   "Pull (object)",
    #     "desc"          :   "Pull an object.",
    #     "need_com_name" :   "no",
    #     "need_com_input":   "no",
    #     "hotkey"        :   ["updateitem"],
    #     "requirements"  :   {},
    #     "func"          :   update_all_items,
    #     "access_level"  :   "admin"},
    
    # "updateplayer": {
    #     "name"          :   "updateplayer",
    #     "cmd_title"     :   "Pull Object",
    #     "cmd_usage"     :   "Pull (object)",
    #     "desc"          :   "Pull an object.",
    #     "need_com_name" :   "no",
    #     "need_com_input":   "no",
    #     "hotkey"        :   ["updateplayer"],
    #     "requirements"  :   {},
    #     "func"          :   update_player,
    #     "access_level"  :   "admin"},

    ## ACTION VERBS

    # "pull": {
    #     "name"          :   "pull",
    #     "cmd_title"     :   "Pull Object",
    #     "cmd_usage"     :   "Pull (object)",
    #     "desc"          :   "Pull an object.",
    #     "need_com_name" :   "no",
    #     "need_com_input":   "yes",
    #     "hotkey"        :   ["pull"],
    #     "requirements"  :   {
    #                         "round_time"    : {
    #                             "req"           : True, 
    #                             "func"          : Status_Check.round_time},
    #                         "is_alive_self" : {
    #                             "req"           : True, 
    #                             "func"          : Status_Check.is_alive_self},
    #                         "target"        : {
    #                             "req"           : None, 
    #                             "func"          : Status_Check.target_required},
    #                         },

    #     "func"          :   Item.action_pull},


    ## ADMIN

    "spawn": {
        "name"          :   "spawn",
        "cmd_title"     :   "Admin: Spawn",
        "cmd_usage"     :   "spawn (npc_type)",
        "desc"          :   "Spawn an npc of designated type in the same room.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "hotkey"        :   ["spawn"],
        "requirements"  :   {
                            "is_admin": {
                                "req": True, 
                                "func": Status_Check.is_admin}
                            },
        "func"          :   Admin_Cmd.spawn},

    "instance": {
        "name"          :   "instance",
        "cmd_title"     :   "Admin: Create Instance",
        "cmd_usage"     :   "spawn (npc_type)",
        "desc"          :   "Create a procedurally generated instance of rooms.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "hotkey"        :   ["instance"],
        "requirements"  :   {
                            "is_admin": {
                                "req": True, 
                                "func": Status_Check.is_admin}
                            },
        "func"          :   Admin_Cmd.create_instance},

    #########

    ## COMBAT

    "attack": {
        "name"          :   "attack",
        "cmd_title"     :   "Attack",
        "cmd_usage"     :   "attack (target)",
        "desc"          :   "Attack at a target. You may use any object. Not using an object results in use of the fist.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["attack"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "target": {
                                "req": None, 
                                "func": Status_Check.target_required},
                            "target_valid": {
                                "req": True, 
                                "func": Status_Check.target_valid},
                            "is_alive_target": {
                                "req": True, 
                                "func": Status_Check.is_alive_target},
                            "is_npc": {
                                "req": True, 
                                "func": Status_Check.is_npc},
                             },
        "func"          :   Combat.attack},

    "fire": {
        "name"          :   "fire",
        "cmd_title"     :   "Fire",
        "cmd_usage"     :   "fire (target)",
        "desc"          :   "Fire at a target. You must have a gun equipped in your right hand.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["fire"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "target": {
                                "req": None, 
                                "func": Status_Check.target_required},
                            "target_valid": {
                                "req": True, 
                                "func": Status_Check.target_valid},
                            "is_alive_target": {
                                "req": True, 
                                "func": Status_Check.is_alive_target},
                            "is_npc": {
                                "req": True, 
                                "func": Status_Check.is_npc},
                            "is_gun": {
                                "req": True, 
                                "func": Status_Check.is_gun},
                            "has_ammo": {
                                "req": True, 
                                "func": Status_Check.has_ammo}
                             },
        "func"          :   Combat.fire_gun},

    #########

    "look": {
        "name"          :   "look",
        "cmd_title"     :   "Look",
        "cmd_usage"     :   "'L' or 'L' (target).",
        "desc"          :   "Inspect something, someone, or the room.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "hotkey"        :   ["l", "look", "exam", "examine"],
        "help"          :   "|success| HELP: |successx| You can use L, LOOK, EXAM, or EXAMINE to look at the room, something else, or someone else.",
        "requirements"  :   {},
        "func"          :   look},
    
    "smile": {
        "name"          :   "smile",
        "cmd_title"     :   "Smile",
        "cmd_usage"     :   "Smile <target>",
        "desc"          :   "Smile verb.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "hotkey"        :   ["smile"],
        "requirements"  :   {
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            },
        "func"          :   Lex.smile},
    
    "north": {
        "name"          :   "north",
        "cmd_title"     :   "Navigate North",
        "cmd_usage"     :   "N",
        "desc"          :   "Travel north.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["n", "north"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand",
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "east": {
        "name"          :   "east",
        "cmd_title"     :   "Navigate East",
        "cmd_usage"     :   "E",
        "desc"          :   "Navigate towards the east compass direction or exit.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["e", "east"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "south": {
        "name"          :   "south",
        "cmd_title"     :   "Navigate South",
        "cmd_usage"     :   "S",
        "desc"          :   "Navigate towards the south compass direction or exit.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["s", "south"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "west": {
        "name"          :   "west",
        "cmd_title"     :   "Navigate West",
        "cmd_usage"     :   "W",
        "desc"          :   "Navigate towards the west compass direction or exit.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["w", "west"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "out": {
        "name"          :   "out",
        "cmd_title"     :   "Navigate Out",
        "cmd_usage"     :   "Out",
        "desc"          :   "Travel out.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["o", "out"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "up": {
        "name"          :   "up",
        "cmd_title"     :   "Navigate Up",
        "cmd_usage"     :   "Up",
        "desc"          :   "Travel up.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["u", "up"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "down": {
        "name"          :   "down",
        "cmd_title"     :   "Navigate Down",
        "cmd_usage"     :   "Down",
        "desc"          :   "Travel down.",
        "need_com_name" :   "yes",
        "need_com_input":   "no",
        "hotkey"        :   ["d", "down"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req": True, 
                                "func": Status_Check.is_alive_self},
                            "stance": {
                                "req": "stand", 
                                "func": Status_Check.stance}
                            },
        "func"          :   Character.navigate},
    
    "i": {
        "name"          :   "inventory",
        "cmd_title"     :   "Inventory",
        "cmd_usage"     :   "I",
        "desc"          :   "Display your inventory.",
        "need_com_name" :   "no",
        "need_com_input":   "no",
        "hotkey"        :   ["i"],
        "requirements"  :   {},
        "func"          :   Player.display_inventory},
    
    # "help": {
    #     "name"          :   "help",
    #     "cmd_title"     :   "Help",
    #     "cmd_usage"     :   "l; l <player>; l <object>.",
    #     "desc"          :   "Show all available commands.",
    #     "need_com_name" :   "no",
    #     "need_com_input":   "no",
    #     "hotkey"        :   "help",
    #     "requirements"  :   {},
    #     "func"          :   func_help},
    
    "get": {
        "name"          :   "get",
        "cmd_title"     :   "Get Object",
        "cmd_usage"     :   "Get (object)",
        "desc"          :   "Pickup an item (right hand always assessed first, then left).",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "hotkey"        :   ["get", "take"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req"   : True, 
                                "func"  : Status_Check.is_alive_self},
                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},

                            "movable": {
                                "req"   :   0, 
                                "func"  :   Status_Check.movable},

                            "is_worn": {
                                "req"   :   False, 
                                "func"  :   Status_Check.is_worn},

                            "one_hand_free": {
                                "req"   :   None, 
                                "func"  :   Status_Check.one_hand_free}
                            },
        "func"          :   Character.get_item},
    
    "drop": {
        "name"          :   "drop",
        "cmd_title"     :   "Drop Object",
        "cmd_usage"     :   "Drop (object)",
        "desc"          :   "Drop an item.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["drop"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req"   : True, 
                                "func"  : Status_Check.is_alive_self},

                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required}
                            },
        "func"          :   Character.drop_item},

    "put": {
        "name"          :   "put",
        "cmd_title"     :   "Put",
        "cmd_usage"     :   "Put (object) in (other object)",
        "desc"          :   "Put one item inside of another.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["put"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self": {
                                "req"   : True, 
                                "func"  : Status_Check.is_alive_self},

                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},

                            "is_worn": {
                                "req"   :   False, 
                                "func"  :   Status_Check.is_worn},

                            "container_is_open": {
                                "req"   :   True, 
                                "func"  :   Status_Check.item_open_closed}
                            },
        "func"          :   Character.put_item},
    
    "'": { 
        "name"          :   "say",
        "cmd_title"     :   "Say / Speak to everyone the room",
        "cmd_usage"     :   "'(your speech)",
        "desc"          :   "Simply type the ' followed directly by what you want your character to say aloud.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["'", "say"],
        "requirements"  :   {},
        "func"          :   Character.say},
    
    "load": {
        "name"          :   "load",
        "cmd_title"     :   "Weapon Load",
        "cmd_usage"     :   "Load (weapon)",
        "desc"          :   "Load your item with ammo. Item must be in the right hand and ammo in the left.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["load"],
        "requirements"  :   {
                            "round_time": {
                                "req": True, 
                                "func": Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target"    : {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},
                            "holding"   : {
                                "req"   :   True, 
                                "func"  :   Status_Check.holding_target},
                            "is_gun"    : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_gun},
                            "has_ammo"  : {
                                "req"   :   False, 
                                "func"  :   Status_Check.has_ammo}
                            },
        "func"          :   Gun.ammo_load},
    
    "unload": {
        "name"          :   "unload",
        "cmd_title"     :   "Weapon Unload",
        "cmd_usage"     :   "Unload (weapon)",
        "desc"          :   "Unload the ammo from your item. Item must be in the right hand and ammo in the left.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["unload"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},
                            "holding": {
                                "req"   :   True, 
                                "func"  :   Status_Check.holding_target},
                            "has_ammo": {
                                "req": True, 
                                "func": Status_Check.has_ammo}
                            },
        "func"          :   Gun.ammo_unload},
    
    "check": {
        "name"          :   "check",
        "cmd_title"     :   "Weapon Ammo Check",
        "cmd_usage"     :   "Check (weapon)",
        "desc"          :   "Check your item's current ammo count. Item must be in the right hand.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["check"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req": None, 
                                "func": Status_Check.target_required},
                            "has_ammo": {
                                "req": True, 
                                "func": Status_Check.has_ammo}
                            },
        "func"          :   Gun.ammo_check},
    
    "stow_set": {
        "name"          :   "stow",
        "cmd_title"     :   "Stow",
        "cmd_usage"     :   "stow (item)",
        "desc"          :   "Put an item in a container set as your stow container. When you STOW SET (CONTAINER), this becomes set as the location you wil automatically put things when you STOW (ITEM) from your hand.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["stow"],
        "requirements"  :   {
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self}
                            },
        "func"          :   Player.stow_set},

    "search": {
        "name"          :   "search",
        "cmd_title"     :   "Search",
        "cmd_usage"     :   "Search (target)",
        "desc"          :   "Search a dead target or search the room/item (not implemented).",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["search"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req": None, 
                                "func": Status_Check.target_required},
                            "target_valid": {
                                "req": True, 
                                "func": Status_Check.target_valid},
                            "is_alive_target": {
                                "req": False, 
                                "func": Status_Check.is_alive_target}
                            },
        "func"          :   Character.search_target},

    "swap": {
        "name"          :   "swap",
        "cmd_title"     :   "Swap",
        "cmd_usage"     :   "Swap",
        "desc"          :   "Swap the items in your hands.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["swap"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self}
                            },
        "func"          :   Character.swap_hands},
    
    "go": {
        "name"          :   "go",
        "cmd_title"     :   "Go",
        "cmd_usage"     :   "Go (object)",
        "desc"          :   "Enter a door or object.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["go"],
        "help"          :   "|success| HELP: |successx| GO (object), e.g. go wagon, go door, go shuttle. Otherwise, to navigate rooms, just use north, n, out, o, etc.",
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required}},
        "func"          :   Character.enter_door},
    
    "open": {
        "name"          :   "open",
        "cmd_title"     :   "Open",
        "cmd_usage"     :   "Open (object)",
        "desc"          :   "Open an object.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["open"],
        "help"          :   "|success| HELP: |successx| OPEN (item) or CLOSE (item). Some objects have special properties, such as ships. Ships may require that you speak to the computer, such as: 'computer, close'. ",
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},
                             "item_open_closed": {
                                "req"   :   "open", 
                                "func"  :   Status_Check.item_open_closed}},
        "func"          :   Item.open_close},
    
    "close": {
        "name"          :   "close",
        "cmd_title"     :   "Close",
        "cmd_usage"     :   "Close (object)",
        "desc"          :   "Close an object.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["close"],
        "help"          :   "|success| HELP: |successx| OPEN (item) or CLOSE (ITEM). Some objects have special properties, such as ships. Ships may require that you speak to the computer, such as: 'computer, close'. ",
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target": {
                                "req"   : None, 
                                "func"  : Status_Check.target_required},
                             "item_open_closed": {
                                "req"   :   "close", 
                                "func"  :   Status_Check.item_open_closed}},
        "func"          :   Item.open_close},
    
    "comm": {
        "name"          :   "comm",
        "cmd_title"     :   "Comm",
        "cmd_usage"     :   "Comm (your speech)",
        "desc"          :   "Communicate via long-distance communication. This speaks out to everyone on the server rather than everyone in the room. You must have a working Comm that is turned on to perform this action and to receive other Comms.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["comm"],
        "requirements"  :   {
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self}
                            },
        "func"          :   Character.comms},
    
    ## SKILLS

    # "climb": {
    #     "name"          :   "climb",
    #     "cmd_title"     :   "Climb",
    #     "cmd_usage"     :   "Climb (object); Climb (direction)",
    #     "desc"          :   'If you see an object that you can climb, simply "climb wall", for example. Once on that object, you can climb up, down, left, or right to navigate the wall. You will have to learn how to navigate these obstacles to minimize injury. Different objects have different difficulty levels.',
    #     "need_com_name" :   "no",
    #     "need_com_input":   "yes",
    #     "req_target"    :   "no",
    #     "hotkey"        :   ["climb"],
    #     "requirements"  :   {
    #                         "round_time": {
    #                             "req"   : True, 
    #                             "func"  : Status_Check.round_time},
    #                         "is_alive_self"  : {
    #                             "req"   :   True, 
    #                             "func"  :   Status_Check.is_alive_self},
    #                         "hands_free": {
    #                             "req": None, 
    #                             "func": Status_Check.hands_free}
    #                         },
    #     "func"          :   Skill.climb},
    
    ## PLAYER INV

    "wear": {
        "name"          :   "wear",
        "cmd_title"     :   "Wear",
        "cmd_usage"     :   "Wear (item)",
        "desc"          :   "Wear an item on your character. Each item fits in a particular inventory slot on your character.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["wear"],
        "requirements"  :   {
                            "round_time": {
                                "req"   :   True, 
                                "func"  :   Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target"    : {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},
                            "holding"   : {
                                "req"   :   True, 
                                "func"  :   Status_Check.holding_target},
                            "is_wearable": {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_wearable},
                            "is_worn"   : {
                                "req"   :   False, 
                                "func"  :   Status_Check.is_worn}
                            },
        "func"          :   Character.wear_item},

    "remove": {
        "name"          :   "remove",
        "cmd_title"     :   "Remove",
        "cmd_usage"     :   "remove (object)",
        "desc"          :   "Remove an item from your inventory.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "yes",
        "hotkey"        :   ["remove", "rem"],
        "requirements"  :   {
                            "round_time": {
                                "req"   :   True, 
                                "func"  :   Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            "target"    : {
                                "req"   :   None, 
                                "func"  :   Status_Check.target_required},
                            "is_worn"   : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_worn}
                            },
        "func"          :   Character.remove_item},

    ## STANCE

    "stand": {
        "name"          :   "stand",
        "cmd_title"     :   "Stand",
        "cmd_usage"     :   "Stand",
        "desc"          :   "Stand up.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["stand"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            },
        "func"          :   Character.change_stance},
    
    "sit": {
        "name"          :   "sit",
        "cmd_title"     :   "Sit",
        "cmd_usage"     :   "Sit",
        "desc"          :   "Sit down.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["sit"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            },
        "func"          :   Character.change_stance},
    
    "lie": {
        "name"          :   "lie",
        "cmd_title"     :   "Lie",
        "cmd_usage"     :   "Lie",
        "desc"          :   "Lie down.",
        "need_com_name" :   "no",
        "need_com_input":   "yes",
        "req_target"    :   "no",
        "hotkey"        :   ["lie"],
        "requirements"  :   {
                            "round_time": {
                                "req"   : True, 
                                "func"  : Status_Check.round_time},
                            "is_alive_self"  : {
                                "req"   :   True, 
                                "func"  :   Status_Check.is_alive_self},
                            },
        "func"          :   Character.change_stance},

    ## HOLODECK

    # "start_simulation": {
    #     "name"          :   "fire",
    #     "cmd_title"     :   "Fire",
    #     "cmd_usage"     :   "fire (target)",
    #     "desc"          :   "Fire at a target. You must have a gun equipped in your right hand.",
    #     "need_com_name" :   "no",
    #     "need_com_input":   "yes",
    #     "req_target"    :   "yes",
    #     "hotkey"        :   "fire",
    #     "requirements"  :   {
    #                          },
    #     "func"          :   Combat.fire_gun}
}
