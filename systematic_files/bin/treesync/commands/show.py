"""
Treesync 'show' subcommand
"""

from .base import TreesyncCommand


class Show(TreesyncCommand):
    """
    Show configured target
    """
    name = 'show'

    def register_parser_arguments(self, parser):
        """
        Register only common base arguments
        """
        return super().register_common_arguments(parser)

    def print_target_details(self, target):
        """
        Print details for target
        """
        pull_command = ' '.join(target.get_pull_command_args())
        push_command = ' '.join(target.get_push_command_args())
        self.message(f'name:          {target.name}')
        self.message(f'source:        {target.source}')
        self.message(f'destitination: {target.destination}')
        self.message(f'iconv:         {target.settings.iconv}')
        self.message(f'excludes file: {target.settings.excludes_file}')
        self.message(f'excludes:      {target.settings.excludes}')
        self.message(f'pull command:  {pull_command}')
        self.message(f'push command:  {push_command}')

    def run(self, args):
        """
        Show details for named targets
        """
        targets = self.filter_targets(args.targets)
        if not targets:
            targets = self.config.sync_targets
        for target in targets:
            self.print_target_details(target)
