import yaml

class Config:
    def __init__(self, filepath: str):
        with open(filepath) as f:
            parsed = yaml.full_load(f).get("config")

        self.CONSUMER_KEY: str = parsed.get("consumer_key")
        self.CONSUMER_SECRET: str = parsed.get("consumer_secret")

        if self.CONSUMER_KEY is None or self.CONSUMER_SECRET is None:
            raise Exception("Consumer key or secret not provided in config")

CONFIG = Config("config/config.yaml")
