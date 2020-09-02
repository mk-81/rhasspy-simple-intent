from ..BaseIntentHandler import BaseIntentHandler
import random
import os

class IntentHandler(BaseIntentHandler): 
	async def handle(self, intent, result) -> None:
		replies = ['Hey Ho!', 'Hallo!', 'Grüße.']
		result.speak(random.choice(replies))
