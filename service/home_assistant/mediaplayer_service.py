from .base import AbstractService

class MediaplayerService(AbstractService):
	async def _call_simple_action(self, action, entity_id):
		response = await self._call_service("media_player", action, entity_id)
		return ( response.status == 200 or response.status == 201 )

	async def play(self, entity_id):
		return await self._call_simple_action("media_play", entity_id)

	async def pause(self, entity_id):
		return await self._call_simple_action("media_pause", entity_id)

	async def stop(self, entity_id):
		return await self._call_simple_action("media_stop", entity_id)

	async def next_track(self, entity_id):
		return await self._call_simple_action("media_next_track", entity_id)

	async def previous_track(self, entity_id):
		return await self._call_simple_action("media_previous_track", entity_id)

	async def turn_on(self, entity_id):
		return await self._call_simple_action("turn_on", entity_id)

	async def turn_off(self, entity_id):
		return await self._call_simple_action("turn_off", entity_id)
