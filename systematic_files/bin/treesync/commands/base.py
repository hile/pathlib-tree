
from systematic_cli.command import Command

from systematic_files.sync.configuration import Configuration


class TreesyncCommand(Command):
    """
    Common base class for treesync subcommands
    """
    config = None

    @staticmethod
    def register_common_arguments(parser):
        """
        Add parser arguments common to all commands
        """
        parser.add_argument('--config', help='Configuration file path')
        parser.add_argument('targets', nargs='*', help='Sync command targets')
        return parser

    def register_rsync_arguments(self, parser):
        """
        Register arguments specific to rsync commands (pull/push)
        """
        parser = self.register_common_arguments(parser)
        parser.add_argument(
            '-y', '--dry-run',
            action='store_true',
            help='Run rsync with --dry-run flag'
        )
        return parser

    def parse_args(self, args):
        self.config = Configuration(args.config)
        return args

    def filter_targets(self, target_names):
        """
        Filter target names
        """
        targets = []
        for name in target_names:
            try:
                target = self.config.get_target(name)
                targets.append(target)
            except ValueError:
                self.error(f'No such target: {name}')
        return targets
