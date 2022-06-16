import yaml

from creatable.source.file import FileSource


class YamlSource(FileSource):
    type = "yaml"

    def read(self):
        with open(self.file_path, "r") as f:
            self.content = yaml.load(f, Loader=yaml.FullLoader)
