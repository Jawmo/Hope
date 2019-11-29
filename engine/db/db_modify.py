from engine.global_config import *
from engine.db_commands import update_db_item, update_db_player

def update_all_items(self):

    for item in items:
        if items[item].uuid_id == "70306652-fbda-479a-a06d-48b411911ed7":
            update_db_item(items[item])
        else:
            print("passing")

def update_player(self):

    for player in players:
        if players[player].uuid_id == self.uuid_id:
            update_db_player(self)
        else:
            print("passing")