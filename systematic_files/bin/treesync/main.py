
from systematic_cli.script import Script

from .commands.pull import Pull
from .commands.push import Push


class Treesync(Script):
    """
    CLI command 'treesync' main  entrypoint
    """
    subcommands = (
        Pull,
        Push
    )


def main():
    """
    CLI command 'treesync' main  entrypoint
    """
    Treesync().run()
