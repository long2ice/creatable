from typing import Any, List, Union, Optional

from creatable.schema import Field, Table
from creatable.source import BaseSource, Config


class FileConfig(Config):
    path: str
    type: str
    name: str
    fields: Optional[List[Union[str, Field]]]

    @property
    def fields_map(self) -> dict:
        ret = {}
        for field in self.fields:
            if isinstance(field, str):
                ret[field] = field
            else:
                ret[field.name] = field
        return ret


class FileSource(BaseSource):
    config_cls = FileConfig
    type = "file"
    config: FileConfig
    content: Any

    def __init__(self, config: dict):
        super().__init__(config)
        self.read()

    def read(self):
        with open(self.file_path, "r") as f:
            self.content = f.read()

    @property
    def file_path(self):
        return self.config.path

    def inspect(self) -> Table:
        fields = []
        content = self.content
        if isinstance(self.content, list):
            content = self.content[0]

        for k, v in content.items():
            if self.config.fields:
                field = self.config.fields_map.get(k)
                if not field:
                    continue
            else:
                field = k
            if isinstance(field, str):
                field = Field(
                    name=k,
                    type=type(v),
                    pk=k == self.config.pk,
                )
            fields.append(field)
        return Table(name=self.config.name, fields=fields, comment=self.config.comment)
