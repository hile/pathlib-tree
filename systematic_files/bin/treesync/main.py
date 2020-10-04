
from systematic_cli.script import Script

from .commands.list import List
from .commands.pull import Pull
from .commands.push import Push
from .commands.show import Show


class Treesync(Script):
    """
    CLI command 'treesync' main  entrypoint
    """
    subcommands = (
        List,
        Pull,
        Push,
        Show,
    )


def main():
    """
    CLI command 'treesync' main  entrypoint
    """
    Treesync().run()
