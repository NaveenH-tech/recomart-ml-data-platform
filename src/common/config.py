from pathlib import Path
import yaml


class Config:

    def __init__(self):

        with open("config/config.yaml") as f:

            self.settings = yaml.safe_load(f)

    def get(self, key):

        return self.settings.get(key)
