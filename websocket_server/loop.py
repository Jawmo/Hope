
def Loop():
	for room in rooms:
	    if rooms[room].player_inv == []:
	        pass
	    else:
	        for npc in rooms[room].npc_inv:
	            npc.npc_state['awake'] = True
	            print(npc.name)
	            s.enterabs(time.time() + 10, 1, Npc.npc_assess, kwargs={"self": npc})