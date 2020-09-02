from .base import AbstractService

class SceneService(AbstractService):
	async def turn_on(self, entity_id):
		response = await self._call_service("scene", "turn_on", entity_id)
		return ( response.status == 200 or response.status == 201 )

