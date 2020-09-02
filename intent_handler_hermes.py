import typing
from uuid import uuid4


from rhasspyhermes.base import Message
from rhasspyhermes.client import GeneratorType, HermesClient
from rhasspyhermes.handle import HandleToggleOff, HandleToggleOn
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes.tts import TtsSay

from intent_dispatcher import Intent_Dispatcher, Intent_Result 
from global_configuration import GlobalConfiguration

import logging

_LOGGER = logging.getLogger("IntentHandlerHermesMqtt_hermes")

class IntentHandlerHermesMqtt(HermesClient):
    def __init__(
        self,
        client,
        global_configuration,
        site_ids: typing.Optional[typing.List[str]] = None,
    ):
        super().__init__("IntentHandlerHermesMqtt_hermes", client, site_ids=site_ids)
        self.handle_enabled = True

        self._intent_dispatcher = Intent_Dispatcher( 
                                      global_configuration=global_configuration,
                                      logger=_LOGGER
                                  )
        self._intent_dispatcher.initialize()

        self.subscribe(NluIntent, HandleToggleOn, HandleToggleOff)

    def set_debug(self, debug=True):
        self._intent_dispatcher.set_debug(debug)

    async def handle_intent(
        self, intent: NluIntent
    ) -> typing.AsyncIterable[typing.Union[TtsSay]]: 
        tts_text = ""
        intent_dict = intent.to_rhasspy_dict()

        # Add site_id
        intent_dict["site_id"] = intent.site_id

        intent_result = Intent_Result()
        await self._intent_dispatcher.dispatch(intent_dict, intent_result)

        # Check for speech response
        result = intent_result.get_result()
        if result:
            tts_text = result.get("speech", {}).get("text", "")


        if tts_text:
            # Forward to TTS system
            yield TtsSay(
                text=tts_text,
                id=str(uuid4()),
                site_id=intent.site_id,
                session_id=intent.session_id,
            )


    async def on_message(
        self,
        message: Message,
        site_id: typing.Optional[str] = None,
        session_id: typing.Optional[str] = None,
        topic: typing.Optional[str] = None,
    ) -> GeneratorType:
        if isinstance(message, NluIntent):
            async for intent_result in self.handle_intent(message):
                yield intent_result
        elif isinstance(message, HandleToggleOn):
            self.handle_enabled = True
        elif isinstance(message, HandleToggleOff):
            self.handle_enabled = False
            
