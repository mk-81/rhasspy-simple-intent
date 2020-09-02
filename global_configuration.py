import os
import json

class _SectionProxy:
    def __init__(self, configuration, section):
        self._configuration = configuration
        self._section       = section

    @property
    def rhasspy_profile_dir(self):
        return self._configuration.rhasspy_profile_dir

    def get_rhasspy_profile_value(self, value_path):
        return self._configuration.get_rhasspy_profile_value(value_path)

    def section_proxy(self, section):
        return _SectionProxy(self, self._section + "." + section)


class GlobalConfiguration:
    def __init__(self, rhasspy_profile_dir):
        self._rhasspy_profile_dir = rhasspy_profile_dir
        self._rhasspy_profile = {}

    def load(self):
        profile_file_name = os.path.join(self._rhasspy_profile_dir, "profile.json")
        if os.path.isfile(profile_file_name):
            with open(profile_file_name, mode='r') as file:
                self._rhasspy_profile = json.load(file)

    @property
    def rhasspy_profile_dir(self):
        return self._rhasspy_profile_dir

    def get_rhasspy_profile_value(self, value_path):
        if isinstance(value_path, str):
            return self.get_rhasspy_profile_value(value_path.split("."))
        else:
            value = self._rhasspy_profile
            for s in value_path:
                if s in value:
                    value = value[s]
                else:
                    return None
            
            return value

    def section_proxy(self, section):
        return _SectionProxy(self, section)
