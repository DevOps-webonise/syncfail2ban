import yaml

class Settings:

    @staticmethod
    def get_config(file):
        return yaml.load(open(file), Loader=yaml.FullLoader)
