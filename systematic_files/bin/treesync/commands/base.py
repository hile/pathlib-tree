
from systematic_cli.command import Command

from systematic_files.sync.configuration import Configuration


class TreesyncCommand(Command):
    """
    Common base class for treesync subcommands
    """
    config = None

    @staticmethod
    def register_parser_arguments(parser):
        """
        Add parser arguments common to all commands
        """
        parser.add_argument('--config', help='Configuration file path')
        parser.add_argument('targets', nargs='*', help='Sync command targets')

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
