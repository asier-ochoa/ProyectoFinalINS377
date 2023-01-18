import json
import os.path

config_template = {
    "mariadb": {
        "host": "",
        "port": 3306,
        "user": "",
        "password": "",
        "database": ""
    },
    "server": {
        "port": 5000
    }
}


class Configurator:

    class Mariadb:
        def __init__(self):
            self.host: None | str = None
            self.port: None | int = None
            self.user: None | str = None
            self.password: None | str = None
            self.database: None | str = None

    class Server:
        def __init__(self):
            self.port: None | int = None

    def __init__(self):
        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                json.dump(config_template, f, indent=4)
                print("Warning: Generated missing config.json, please fill it out and relaunch the program")
                exit(0)

        with open("config.json", "r") as f:
            conf_dict: dict = json.load(f)
            conf_template_dict_keys = [a for a in config_template["mariadb"].keys()] + [a for a in config_template["server"].keys()]

            if any([x == "" for x in [a for a in conf_dict["mariadb"].values()] + [a for a in conf_dict["server"].values()] if isinstance(x, str)]):
                print("Error: Empty values in config.json file! Exiting program")
                exit(1)

            if any([x not in [a for a in conf_dict["mariadb"].keys()] + [a for a in conf_dict["server"].keys()] for x in conf_template_dict_keys]):
                print("Error: Missing keys in config.json file! Exiting program")
                exit(1)

        self.mariadb = self.Mariadb()
        self.mariadb.host = conf_dict['mariadb']['host']
        self.mariadb.port = conf_dict['mariadb']['port']
        self.mariadb.user = conf_dict['mariadb']['user']
        self.mariadb.password = conf_dict['mariadb']['password']
        self.mariadb.database = conf_dict['mariadb']['database']

        self.server = self.Server()
        self.server.port = conf_dict['server']['port']


def _setattr_override(self, key, value):
    raise AttributeError("Can't set configuration values!")


config = Configurator()
Configurator.__setattr__ = _setattr_override
