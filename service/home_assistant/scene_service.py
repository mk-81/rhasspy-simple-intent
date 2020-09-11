from .base import AbstractService

class SceneService(AbstractService):
	def _init_int(self):
		self._service_name = "scene"
		self._default_entity_name = "scene"

	async def turn_on(self, entity_id):
		response = await self._call_service("turn_on", entity_id)
		return ( response.status == 200 or response.status == 201 )

