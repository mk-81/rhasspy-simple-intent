from ..BaseIntentHandler import BaseIntentHandler
import datetime

class IntentHandler(BaseIntentHandler):
	async def handle(self, intent, result):
		now = datetime.datetime.now()
		if now.minute == 0:
			result.speak("Es ist %d Uhr" % (now.hour))
		else:
			result.speak("Es ist %d Uhr %d" % (now.hour, now.minute))
