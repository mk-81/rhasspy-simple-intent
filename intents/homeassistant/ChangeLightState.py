import asyncio
from ..BaseIntentHandler import BaseIntentHandler

class IntentHandler(BaseIntentHandler): 
	async def handle(self, intent, result):
		entity_id = None
		ha_service = self.services.home_assistant.get_instance()

		if "entity_id" in intent["slots"]:
			entity_id = intent["slots"]["entity_id"]
			
		if entity_id == None or entity_id == "":
			return
			
		state = intent["slots"]["state"]
		
		entity_ids = entity_id.split()

		calls = []
		
		for entity_id in entity_ids:
			if state == "on":
				calls.append( ha_service.light.turn_on(entity_id) )
			elif state == "off":
				calls.append( ha_service.light.turn_off(entity_id) )
			else:
				return

		cr = True
		crs = await asyncio.gather(*calls, return_exceptions=True)
		for r in crs:
			cr = cr and r
			
		if cr == False:
			result.speak("das licht kenne ich nicht")
