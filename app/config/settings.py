import yaml

class Settings:
    def __init__(self, file_path="config.yaml"):
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)

        self.HOST = config["server"]["host"]
        self.PORT = config["server"]["port"]
        self.GRPC_PORT = config["server"]["grpc_port"]
        self.MODELS = config["models"]

settings = Settings()
