from .base import AbstractService

class LightService(AbstractService):
	async def switch_light(self, entity_id, on_off):
		if on_off:
			action = "turn_on"
		else:
			action = "turn_off"
		
		response = await self._call_service("light", action, entity_id)
		return ( response.status == 200 or response.status == 201 )
	

	async def turn_on(self, entity_id):
		return await self.switch_light(entity_id, True)

	async def turn_off(self, entity_id):
		return await self.switch_light(entity_id, False)
