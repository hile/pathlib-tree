"""
Treesync 'pull' subcommand
"""

from .base import TreesyncCommand


class Pull(TreesyncCommand):
    """
    Tree pull subcommand
    """
    name = 'pull'

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
            self.message(f'pull {target.destination} -> {target.source}')
            target.pull(dry_run=args.dry_run)
