from engine.global_config import *
from engine.lex import *

##### Background Events #####

# s.enterabs(time.time() + 60, 1, Recurring_BG.ship_bg_beep)
# s.enter(5, 1, Lex.print_event, kwargs={'self': self})


def initialize_sounds():
    Recurring_BG.ship_bg_beep()

class Recurring_BG():
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func
    
    def ship_bg_beep():
        Lex.pub_print(
            self=self,
            message_type = "speech",
            target=None,
            first_person = "test1st",
            target_person = "",
            third_person = "test3rd")

        return msg_type, msg
        # s.enterabs(time.time() + 5, 1, Recurring_BG.ship_bg_beep)