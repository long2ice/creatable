from creatable.destination import BaseDestination, Config
from creatable.schema import Field


class PostgresConfig(Config):
    database: str
    schema_: str

    class Config:
        fields = {
            "schema_": "schema",
        }


class PostgresDestination(BaseDestination):
    type = "postgres"
    config_cls = PostgresConfig

    @property
    def connection(self):
        pass

    @property
    def create_table_sql(self) -> str:
        pass

    @property
    def field_map(self) -> dict:
        pass

    def field(self, field: Field) -> str:
        pass

    def create(self):
        pass
