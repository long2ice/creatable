from pydantic import BaseModel, Extra
from loguru import logger
from creatable.schema import Table, Field


class Config(BaseModel):
    host: str
    port: int
    user: str
    password: str

    class Config:
        extra = Extra.allow


class BaseDestination:
    type: str = "base"
    config_cls = Config
    config: Config

    def __init__(self, config: dict, table: Table):
        self.table = table
        self.config = self.config_cls.parse_obj(config)

    @property
    def connection(self):
        raise NotImplementedError

    @property
    def create_table_sql(self) -> str:
        raise NotImplementedError

    @property
    def field_map(self) -> dict:
        raise NotImplementedError

    def field(self, field: Field) -> str:
        raise NotImplementedError

    def create(self):
        self.connection.cursor().execute(self.create_table_sql)
