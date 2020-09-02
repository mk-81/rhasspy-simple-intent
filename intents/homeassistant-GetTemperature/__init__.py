from ..BaseIntentHandler import BaseIntentHandler
from service.home_assistant import HA_BadRequestError, HA_UnauthorizedError, HA_NotFoundError

class IntentHandler(BaseIntentHandler): 
	async def handle(self, intent, result):
		ha_service = self.services.home_assistant.get_instance()
		
		if "entity_id" in intent["slots"]:
			entity_id = intent["slots"]["entity_id"]
			
		if entity_id == None or entity_id == "":
			return

		try:
			data = await ha_service.sensors.get_entity_state(entity_id)
			sensor_value = data["state"] 
			if sensor_value == "unavailable":
				result.speak("sensor ist nicht verfügbar")
			else:
				try:
					v = float(sensor_value)
					s = "{} grad".format(v).replace(".", ",")
					result.speak(str(s))
					#result.speak("%f" % (v))
				except ValueError:
					result.speak(sensor_value)

		except HA_BadRequestError:
			raise SystemError()
			
		except HA_UnauthorizedError:
			raise SystemError()

		except HA_NotFoundError:
			result.speak("Ich kenne den Sensor nicht")
