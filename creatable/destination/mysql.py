import inspect

import MySQLdb

from creatable.destination import BaseDestination, Config
from creatable.schema import Field


class MySQLConfig(Config):
    database: str


class MySQLDestination(BaseDestination):
    type = "mysql"
    config_cls = MySQLConfig
    config: MySQLConfig

    @property
    def connection(self):
        return MySQLdb.connect(
            **self.config.dict(exclude={"type"}),
        )

    @property
    def field_map(self) -> dict:
        return {
            int: "INT",
            str: "VARCHAR(255)",
            bool: "TINYINT(1)",
            float: "FLOAT",
            list: "JSON",
            dict: "JSON",
        }

    def field(self, field: Field) -> str:
        return "`{name}` {type} {nullable} {unique}{primary}{default}{comment}".format(
            name=field.name,
            type=self.field_map[field.type]
            if inspect.isclass(field.type)
            else field.type,
            nullable="NULL" if field.nullable else "NOT NULL",
            unique="UNIQUE" if field.unique else "",
            primary="PRIMARY KEY" if field.pk else "",
            default="DEFAULT {default}".format(default=field.default)
            if field.default
            else "",
            comment="COMMENT '{comment}'".format(comment=field.comment)
            if field.comment
            else "",
        )

    @property
    def create_table_sql(self):
        table = self.table
        fields = [self.field(field) for field in table.fields]
        fields_str = "\n    {}\n".format(",\n    ".join(fields))
        comment = (
            " COMMENT '{comment}'".format(comment=table.comment)
            if table.comment
            else ""
        )
        # TODO
        extra = " "
        return f"CREATE TABLE `{table.name}` ({fields_str}){extra}{comment}"
