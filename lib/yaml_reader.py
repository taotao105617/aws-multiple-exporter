import yaml
import json
import os


class YamlReader:
    def __init__(self, file):
        file_path = os.path.abspath(os.path.join('conf/metrics', file))
        self.file_path = file_path

    def init(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data
