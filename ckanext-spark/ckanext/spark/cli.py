import click


@click.group(short_help="spark CLI.")
def spark():
    """spark CLI.
    """
    pass


@spark.command()
@click.argument("name", default="spark")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [spark]
