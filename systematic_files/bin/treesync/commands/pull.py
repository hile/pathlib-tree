"""
Treesync 'pull' subcommand
"""

from .base import TreesyncCommand


class Pull(TreesyncCommand):
    """
    Tree pull subcommand
    """
    name = 'pull'

    def run(self, args):
        targets = self.filter_targets(args.targets)
        if not targets:
            self.exit(1, 'No targets specified')
        for target in targets:
            self.message('pull', target)
