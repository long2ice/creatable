import json
from typing import Union

from creatable.source.file import FileSource


class JsonSource(FileSource):
    content: Union[list, dict]
    type = "json"

    def read(self):
        with open(self.file_path, "r") as f:
            self.content = json.load(f)
