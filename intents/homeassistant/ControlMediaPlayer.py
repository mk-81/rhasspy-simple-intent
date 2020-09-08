from ..BaseIntentHandler import BaseIntentHandler

class IntentHandler(BaseIntentHandler): 
	async def handle(self, intent, result):
		entity_id = None
		action = None

		slots = intent["slots"]

		if "action" in slots:
			action = slots["action"]

		if "entity_id" in slots:
			entity_id = slots["entity_id"]

		if entity_id == None or entity_id == "" or action == None:
			return

		if action == "turn_on_off":
			await self.handle_turn_on_off(entity_id, slots)

		elif action == "volume":
			await self.handle_turn_on_off(entity_id, slots)

		else:
			await self.handle_action(entity_id, action)

			
	async def handle_turn_on_off(self, entity_id, slots):
		if "state" not in slots:
			return

		state = slots["state"]

		ha_service = self.services.home_assistant.get_instance()

		result = None
		if state == "on":
			result = await ha_service.media_player.turn_on(entity_id)
		elif state == "off":
			result = await ha_service.media_player.turn_off(entity_id)

		return result

	async def handle_action(self, entity_id, action):
		ha_service = self.services.home_assistant.get_instance()

		result = None
		if action == "play":
			result = await ha_service.media_player.play(entity_id)
		elif action == "pause":
			result = await ha_service.media_player.pause(entity_id)
		elif action == "stop":
			result = await ha_service.media_player.stop(entity_id)

		return result