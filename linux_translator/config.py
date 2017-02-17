"""Module contain configuration singleton"""

import json


class Config(dict):
    """Class represent global application configuration"""

    def read(self, fname):
        """Read config file and load attributes from it"""
        with open(fname, 'r') as f:
            conf = f.read()
            self.update(json.loads(conf))

    def write(self, fname):
        with open(fname, 'w') as f:
            f.write(json.dumps(self, default_flow_style=False))


config = Config()
