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

        entity_ids = entity_id.split()

        calls = []
        
        for entity_id in entity_ids:
            entity_domain = ha_service.get_domain_from_entity_id(entity_id)
            service = ha_service.get_service_by_domain(entity_domain)
            if service != None and service.supports("turn_off"):
                calls.append( service.turn_off(entity_id) )


        cr = True
        crs = await asyncio.gather(*calls, return_exceptions=True)
        for r in crs:
            cr = cr and r

        if r == False:
            result.speak("das kann ich nicht machen")
