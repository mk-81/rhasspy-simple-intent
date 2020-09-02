from ..BaseIntentHandler import BaseIntentHandler
import datetime
import random
import os
import json

compliments = None

class IntentHandler(BaseIntentHandler):
    async def handle(self, intent, result):
        global compliments

        if "who" not in intent["slots"]:
            return

        who = intent["slots"]["who"]

        if compliments == None:
            compliments = {}
            path = os.path.dirname(__file__)
            file_name = os.path.join(path, 'compliments.json')
            if os.path.isfile(file_name):
                with open(file_name, mode='r') as file:
                    compliments = json.load(file)
                    file.close()

        if "who" in compliments and who in compliments["who"]:
            list = compliments["who"][who]
        elif "" in compliments:
            list = compliments[""]
        else:
            return

        result.speak(random.choice(list))


