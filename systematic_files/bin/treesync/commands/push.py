"""
Treesync 'push' subcommand
"""

from .base import TreesyncCommand


class Push(TreesyncCommand):
    """
    Tree push subcommand
    """
    name = 'push'

    def register_parser_arguments(self, parser):
        """
        Register arguments for 'pull' command
        """
        return super().register_rsync_arguments(parser)

    def run(self, args):
        targets = self.filter_targets(args.targets)
        if not targets:
            self.exit(1, 'No targets specified')
        for target in targets:
            self.message(f'push {target.source} -> {target.destination}')
            target.push(dry_run=args.dry_run)
