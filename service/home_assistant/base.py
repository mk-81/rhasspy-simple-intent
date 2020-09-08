import aiohttp

from .exceptions import *
import os
import json

class Config():
    def __init__(self, global_configuration):
        self._global_configuration=global_configuration
        
    def load(self):
        self.config = {
            "url" : None,
            "authorizationToken" : None,

        }
        file_name = os.path.join( self._global_configuration.rhasspy_profile_dir, "HomeAssistantConfig.json")
        if os.path.isfile(file_name):
            with open(file_name , "r") as config_file:
                own_config = json.load(config_file)
        else:
            own_config = {}

        if "url" in own_config:
            self.config["url"] = own_config["url"]
        else:
            self.config["url"] = self._global_configuration.get_rhasspy_profile_value("home_assistant.url")

        if "authorizationToken" in own_config:
            self.config["authorizationToken"] = own_config["authorizationToken"]
        else:
            self.config["authorizationToken"] = self._global_configuration.get_rhasspy_profile_value("home_assistant.access_token")

            
    def getServerUrl(self):
        return self.config["url"]
        
    def getServerApiToken(self):
        return self.config["authorizationToken"]


class EndpointService():
    def __init__(self, config):
        self._client_session = None
        self.config = config

    def buildApiEndpointUrl(self, endpoint):
        server_url = self.config.getServerUrl()
        
        if endpoint.startswith("/"):
            return server_url + "/api" + endpoint
        else:
            return server_url + "/api/" + endpoint
        
    def buildApiHttpHeaders(self):
        return {
            "Authorization": "Bearer " + self.config.getServerApiToken(),
            "content-type": "application/json"
        }

    def get_session(self):
        if self._client_session == None:
            self._client_session = aiohttp.ClientSession()
        return self._client_session

    async def finalize(self):
        if self._client_session != None:
            await self._client_session.close()



class AbstractService():
    def __init__(self, endpoint_service):
        self._endpoint_service = endpoint_service
        
    def _is_http_call_successful(self, status_code):
        return ( status_code == 200 or status_code == 201 )
        
    def _handle_http_call_result(self, status_code):
        if status_code == 400 or status_code == 405:
            raise HA_BadRequestError()
            
        elif status_code == 401:
            raise HA_UnauthorizedError()
        
        elif status_code == 404:
            raise HA_NotFoundError()
            
        else:
            raise HA_BadRequestError()

    async def _call_service(self, service, action, entity_id, data = None):
        url     = self._endpoint_service.buildApiEndpointUrl("/services/" + service + "/" + action)
        headers = self._endpoint_service.buildApiHttpHeaders()

        session = self._endpoint_service.get_session()

        call_data = data
        if call_data == None:
            call_data = { "entity_id": entity_id }
        elif entity_id != None:
            call_data["entity_id"] = entity_id
        
        return await session.post(url, headers=headers, json=call_data)

    
    def supports(self, method):
        method = str(method)
        if len(method) == 0 or method[0] == '_':
            return False

        m = getattr(self, method, None)
        return m != None and callable(m)

        
    async def get_entity_state(self, entity_id):
        url     = self._endpoint_service.buildApiEndpointUrl("/states/" + entity_id)
        headers = self._endpoint_service.buildApiHttpHeaders()

        session = self._endpoint_service.get_session()
        
        response = await session.get(url, headers=headers)
        if response.status == 200 or response.status == 201:
            return json.loads(await response.text() )
        else:
            return None

