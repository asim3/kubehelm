from configparser import ConfigParser
from pathlib import Path


class Configuration:
    config_path = Path.home() / '.kubehelm.ini'
    default_config = {"DEBUG": "true"}

    def write_default_config_file(self):
        config = ConfigParser()
        config['GLOBALD'] = self.default_config
        with open(self.config_path, 'w') as config_file:
            config.write(config_file)
            return config

    def get_config_file(self):
        config = ConfigParser()
        if config.read(self.config_path):
            return config
        return self.write_default_config_file()

    def update_config_file(self, name, value):
        config = self.get_config_file()
        config['GLOBALD'][name] = value
        with open(self.config_path, 'w') as config_file:
            config.write(config_file)
            return config["GLOBALD"]

    def get_all(self):
        config = self.get_config_file()
        return config["GLOBALD"]


CONFIG = Configuration().get_all()
