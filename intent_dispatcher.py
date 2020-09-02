import importlib

from services import Services
from service.home_assistant import Home_Assistant_Service
from intents.BaseIntentHandler import BaseIntentHandler
from global_configuration import GlobalConfiguration


class Intent_Result():
	def __init__(self):
		self._result = None

	def speak(self, text):
		self._result = {
			"speech" : {"text": text}
		}

	def get_result(self):
		return self._result


class Intent_Dispatcher():
	def __init__(self, global_configuration, logger):
		self._global_configuration = global_configuration
		self._services = None
		self._handlers = {}
		self._logger = logger
		self._debug = False

	def initialize(self):
		service_conf = self._global_configuration.section_proxy("services")
		self._services = Services(
							home_assistant=Home_Assistant_Service(global_configuration=service_conf.section_proxy("home_assistant"))
						)

	def set_debug(self, debug=True):
		self._debug = debug

	def _create_handler(self, intent_name: str) -> BaseIntentHandler:
		if intent_name not in self._handlers:
			handler_class = None
			try:
				module        = importlib.import_module(".", "intents." + intent_name)
				handler_class = getattr(module, "IntentHandler")
			except ModuleNotFoundError as e:
				self._logger.debug("IntentHandler " + intent_name + " not found")

			except Exception as e:
				self._logger.warning(e)
		
			self._handlers[intent_name] = {
				"handler_class" : handler_class
			}

		handler_info = self._handlers[intent_name]
		handler_class = handler_info.get("handler_class", None)
		if handler_class != None:
			return handler_class(services=self._services)
		else:
			return None


	async def dispatch(self, intent, result: Intent_Result) -> None : 
		intent_name = intent["intent"]["name"]
	
		handler_instance = self._create_handler(intent_name)
		if handler_instance != None:
			await handler_instance.initialize()
			await handler_instance.handle(intent, result)
			await handler_instance.finalize()

	async def finalize(self):
		await self._services.finalize()


