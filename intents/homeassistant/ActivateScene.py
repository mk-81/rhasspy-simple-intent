from ..BaseIntentHandler import BaseIntentHandler

class IntentHandler(BaseIntentHandler): 
	async def handle(self, intent, result):
		entity_id = None
		ha_service = self.services.home_assistant.get_instance()
		
		if "entity_id" in intent["slots"]:
			entity_id = intent["slots"]["entity_id"]
			
		if entity_id == None or entity_id == "":
			return
			
		r = await ha_service.scene.turn_on(entity_id)
		
		if r == False:
			result.speak("das kann ich nicht machen")
