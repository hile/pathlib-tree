"""
Treesync 'push' subcommand
"""

from .base import TreesyncCommand


class Push(TreesyncCommand):
    """
    Tree push subcommand
    """
    name = 'push'

    def run(self, args):
        targets = self.filter_targets(args.targets)
        if not targets:
            self.exit(1, 'No targets specified')
        for target in targets:
            self.message('push', target.source, target.destination)
            target.push()
