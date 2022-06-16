from pydantic import BaseModel

from creatable.schema import Table


class Config(BaseModel):
    pk: str = None
    comment: str = None


class BaseSource:
    config_cls = Config
    config: Config
    type: str

    def __init__(self, config: dict):
        self.config = self.config_cls.parse_obj(config)

    def inspect(self) -> Table:
        raise NotImplementedError
