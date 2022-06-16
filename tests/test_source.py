import pytest

from creatable.source.file.csv import CsvSource
from creatable.source.file.json import JsonSource
from creatable.source.file.yaml import YamlSource
from creatable.utils import discover_source_cls_by_type


def test_discover_source_cls_by_type():
    assert discover_source_cls_by_type("file", "csv") is CsvSource
    assert discover_source_cls_by_type("file", "json") is JsonSource
    assert discover_source_cls_by_type("file", "yaml") is YamlSource

    with pytest.raises(RuntimeError):
        discover_source_cls_by_type("file", "unknown")
