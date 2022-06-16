import typer
import yaml

from creatable.utils import (
    discover_destination_cls_by_type,
    discover_source_cls_by_type,
)


def cli(
    config: typer.FileText = typer.Option(
        "config.yaml", "-c", "--config", help="Configuration file"
    ),
    execute: bool = typer.Option(
        False, "-e", "--execute", help="Execute at the same time"
    ),
):
    config = yaml.load(config, Loader=yaml.FullLoader)
    source = config["source"]
    destination = config["destination"]
    source_type = source["type"]
    source_config = source["config"]
    source_config_type = source_config["type"]
    source_cls = discover_source_cls_by_type(source_type, source_config_type)
    source_obj = source_cls(source_config)
    table = source_obj.inspect()
    destination_cls = discover_destination_cls_by_type(destination["type"])
    destination_obj = destination_cls(destination, table)
    if execute:
        destination_obj.create()
    else:
        typer.secho(destination_obj.create_table_sql)


def main():
    typer.run(cli)


if __name__ == "__main__":
    main()
