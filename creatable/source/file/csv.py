import csv

from creatable.source.file import FileSource


class CsvSource(FileSource):
    type = "csv"

    def read(self):
        content = []
        with open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                content.append(row)
        self.content = content
