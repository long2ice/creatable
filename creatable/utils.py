import importlib
import inspect
from os import listdir
from typing import Type

from creatable.destination import BaseDestination
from creatable.source import BaseSource


def discover_source_cls_by_type(source_type: str, source_config_type: str) -> Type[BaseSource]:
    if source_type == "database":
        module = importlib.import_module("creatable.source.database")
    elif source_type == "file":
        module = importlib.import_module("creatable.source.file")
    else:
        raise RuntimeError("Unknown source type: {}".format(source_type))
    path = module.__path__
    for f in listdir(path[0]):
        if f.endswith(".py") and f != "__init__.py":
            module_name = f[:-3]
            module = importlib.import_module(f"creatable.source.{source_type}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseSource)
                    and obj.type == source_config_type
                ):
                    return obj
    raise RuntimeError(f"Could not find source class for type: {source_config_type}")


def discover_destination_cls_by_type(destination_type: str) -> Type[BaseDestination]:
    module = importlib.import_module("creatable.destination")
    path = module.__path__
    for f in listdir(path[0]):
        if f.endswith(".py") and f != "__init__.py":
            module_name = f[:-3]
            module = importlib.import_module(f"creatable.destination.{module_name}")
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseDestination)
                    and obj.type == destination_type
                ):
                    return obj
    raise RuntimeError(f"Could not find destination class for type: {destination_type}")
