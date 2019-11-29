from engine.ship.ship_main import Ship

ship_ai_cmds = {
	
	"open": {
		
		"cmd_name"	:	"open",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.open_door},

	"close": {
		
		"cmd_name"	:	"close",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.close_door},

	"travel": {
		
		"cmd_name"	:	"takeoff",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.takeoff},

	"takeoff": {
		
		"cmd_name"	:	"close",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.travel}

}