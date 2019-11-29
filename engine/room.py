from pprint import pprint
from engine.global_config import *
from engine.lex import *

from engine.rooms.room_templates import room_templates
from engine.update_client import Update_Client

from websocket_server.wswrap import WsWrap

###### Room Class ######

class Room():
    def __init__(self, **kwargs):
        self.uuid_id =      kwargs['uuid_id']
        self.entity_type =  kwargs['entity_type']
        self.ship_id =      kwargs['ship_id']
        self.coordinates =  kwargs['coordinates']
        self.name =         kwargs['name']
        self.description =  kwargs['description']
        self.exits =        kwargs['exits']
        self.region =       kwargs['region']
        self.zone =         kwargs['zone']
        self.elevation =    kwargs['elevation']
        self.effects =      kwargs['effects']
        self.player_inv =   []
        self.item_inv =     []
        self.npc_inv =      []
        self.mob_inv =      []
        self.owner =        kwargs['owner']
        
    def generate_area(self, user, user_input, input_kwargs):

        area = Room_Procgen.procgen_flow(self)

    def render_map(self, user):

        coord_dict = {}
        map_render = {}

        for each_room in rooms:
            if rooms[each_room].region == rooms[user.location].region:
                if rooms[each_room].zone == rooms[user.location].zone:
                    coord_dict[(rooms[each_room].coordinates['x'], rooms[each_room].coordinates['y'])] = {
                        "exits": rooms[each_room].exits,
                    }
        # print(coord_dict)

        min_width = min(coord_dict, key = lambda t: t[0])[0] * 2
        min_height = min(coord_dict, key = lambda t: t[1])[1] * 2
        max_width = (max(coord_dict, key = lambda t: t[0])[0] + 1) * 2
        max_height = (max(coord_dict, key = lambda t: t[1])[1] + 1) * 2

        print(min_width, max_width, min_height, max_height)

        self_x = rooms[user.location].coordinates['x']
        self_y = rooms[user.location].coordinates['y']
        self_room = (rooms[user.location].coordinates['x'],
                     rooms[user.location].coordinates['y'])


        # print(self_x, self_y, max_width, max_height)
        for y in range(self_y - (max_height // 2), self_y + (max_height // 2)):
            for x in range(self_x - (max_width // 2), self_x + (max_width // 2)):
                # print("Checking:", (x,y))
                if (x,y) in coord_dict and x == rooms[user.location].coordinates['x'] and y == rooms[user.location].coordinates['y']:
                        
                    map_render[(x,y)] = {'symbol': '|y|[x]|yx|'}
                    map_render[(x,y)]['exits'] = coord_dict[(x,y)]['exits']
                
                elif (x,y) in coord_dict:
                       
                    map_render[(x,y)] = {'symbol': '[|black|x|blackx|]'}
                    map_render[(x,y)]['exits'] = coord_dict[(x,y)]['exits']

                else:
                        
                    map_render[(x,y)] = {'symbol': '|black|[x]|blackx|'}
                    map_render[(x,y)]['exits'] = ''

                if "east" in map_render[(x,y)]["exits"]:

                    map_render[(x,y)]['symbol'] = map_render[(x,y)]['symbol'] + '-'
                
                else:

                    map_render[(x,y)]['symbol'] = map_render[(x,y)]['symbol'] + '|black|-|blackx|'

                # if "south" in map_render[(x, y)]["exits"]:
                    
                #     map_render[(x,y)]['symbol'] = map_render[(x,y)]['symbol'] + '|br|-|-'
                
                # else:

                #     map_render[(x,y)]['symbol'] = map_render[(x,y)]['symbol'] + '|br|?'
                

                if x + 1 == self_x + (max_width // 2):
                        
                     map_render[(x,y)]['symbol'] = map_render[(x,y)]['symbol'] + '|br|'


        # print("Coord Dict:", len(coord_dict))
        # print("Final Render:", len(map_render))

        the_map = []
        
        for i in map_render:
            the_map.append(map_render[i]['symbol'])

        the_map = '{}'.format("".join(the_map))

        Update_Client.update_map(user, the_map)

    def display_room(self, user):
        room_num = user.location
        name_list = Gen.players_in_room(user)
        item_list = Gen.items_in_room(user)
        npc_list = Gen.npcs_in_room(user)

        # check if there are items
        if item_list == []:
            pass
        else:
            room_item_list = []
            for i in item_list:
                room_item_list.append(i.name)
            room_item_list = Lex.converted_contents(room_item_list)

        if rooms[user.location].entity_type['group'] == "ship_personal":
            ship_num = rooms[user.location].ship_id
            room_of_ship = rooms[items[ship_num].location]

            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "|room|{} | Outside you see {}|roomx|".format(rooms[room_num].name, Lex.a_an(room_of_ship.name)))
        else:
            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "|room|{} | {}|roomx| | [{},{}]".format(rooms[room_num].region, rooms[room_num].name, rooms[room_num].coordinates['x'], rooms[room_num].coordinates['y']))

        # check if there are items
        if item_list == []:
            if rooms[user.location].entity_type['group'] == "ship_personal":

                room_ship_list = []
                ship_list = Gen.ships_in_room(user)
                for i in ship_list:
                    room_ship_list.append(i.name)
                if room_ship_list == []:    
                    WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0},
                        "{} Outside, {}".format(
                            rooms[room_num].description, 
                            rooms[items[rooms[user.location].ship_id].location].description.lower()))

                else:
                    WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0},
                        "{} Outside, {} You also see the {}.".format(
                            rooms[room_num].description, 
                            rooms[items[rooms[user.location].ship_id].location].description.lower(), 
                            ", ".join(room_ship_list)))

            else:
                WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "{}".format(rooms[room_num].description))
            
        else:
            
            room_item_list = []
            
            for i in item_list:
                if i.static_stats['visible'] == True:
                    room_item_list.append(i.name)
            
            room_item_list = Lex.converted_contents(room_item_list)
            
            if "ship_personal" == rooms[user.location].entity_type['group']:
                WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "{} Outside, {} You also see {}.".format(rooms[room_num].description, rooms[items[rooms[user.location].ship_id].location].description.lower(), ", ".join(room_item_list)))
            else:
                if room_item_list == []:
                    WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "{}".format(rooms[room_num].description))
                else:
                    WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0}, "{} You also see {}.".format(rooms[room_num].description, ", ".join(room_item_list)))
        

        # check for npcs
        if npc_list == []:
            pass
        else:
            room_npc_names = []
            for i in npc_list:
                if i.vitals['alive'] == False:
                    room_npc_names.append("dead " + i.name)
                else:
                    room_npc_names.append(i.name)
            
            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0},
                "You also see |npc| {} |npcx|.".format(", ".join(Lex.converted_contents(room_npc_names))))
        
        # check for other players
        if name_list == []:
            pass
        else:
            room_player_names = []
            for i in name_list:
                if i.client['type'] == "tourist":
                    i.name = "{} {}".format("Tourist", i.name)

                room_player_names.append('{} {}'.format(i.core_attributes['title'], i.name.capitalize()))

            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 0},
                "|room| Also here: |roomx| {}".format(", ".join(room_player_names)))

        # check for obvious exits
        if rooms[room_num].exits == {}:
            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 1},
                "|exits| Exits: |/exits| None")
        else:
            WsWrap.ws_send(user.client, {'type': 'text', 'spacing': 1},
                "|exits| Exits: |/exits| {}".format(", ".join(rooms[room_num].exits)))

        self.render_map(user)

    def convert_rooms_to_obj():
        for i in rooms:
            print(i, rooms[i])
            new_room = Room(i,              # uuid
                            rooms[i][0],    # entity_type
                            rooms[i][1],    # ship_id
                            rooms[i][2],    # coordinates
                            rooms[i][3],    # name
                            rooms[i][4],    # description
                            rooms[i][5],    # exits
                            rooms[i][6],    # region
                            rooms[i][7],    # zone
                            rooms[i][8],    # elevation
                            rooms[i][9],   # effects
                            rooms[i][10],   # player_inv
                            rooms[i][11],   # item_inv
                            rooms[i][12],   # npc_inv
                            rooms[i][13],   # mob_inv
                            rooms[i][14])   # owner
            
            rooms[i] = new_room
            # pprint(vars(new_room))