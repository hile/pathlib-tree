"""
Configuration for 'treesync' CLI application
"""

from systematic_cli.configuration import (
    ConfigurationSection,
    YamlConfiguration
)

from ..tree import SKIPPED_PATHS
from .constants import (
    DEFAULT_CONFIGURATION_PATHS,
    DEFAULT_EXCLUDES,
    DEFAULT_EXCLUDES_FILE,
    DEFAULT_FLAGS,
    TREE_CONFIG_FILE
)
from .target import Target


class Defaults(ConfigurationSection):
    """
    Tree sync default settings
    """
    __name__ = 'defaults'
    __default_settings__ = {
        'rsync_command': 'rsync',
        'flags': DEFAULT_FLAGS,
        'never_sync_paths': SKIPPED_PATHS,
        'excluded_paths': DEFAULT_EXCLUDES,
        'tree_config_file': TREE_CONFIG_FILE,
        'tree_excludes_file': DEFAULT_EXCLUDES_FILE,
    }


class TargetConfiguration(ConfigurationSection):
    """
    Loader for named targets in TargetSettings
    """
    __default_settings__ = {
        'ignore_default_flags': False,
        'ignore_default_excludes': False,
        'excludes': [],
        'excludes_file': None,
        'flags': [],
        'iconv': None,
    }
    __required_settings__ = (
        'source',
        'destination',
    )

    @property
    def destination_server_settings(self):
        """
        Return settings for destination server
        """
        try:
            # pylint: disable=no-member
            host, _path = str(self.destination).split(':', 1)
        except IndexError:
            return None
        # pylint: disable=no-member
        return getattr(self.__config_root__.servers, host, None)

    @property
    def destination_server_flags(self):
        """
        Return flags specific to destination server
        """
        flags = []
        settings = self.destination_server_settings
        if settings is not None:
            iconv = getattr(settings, 'iconv', None)
            if iconv is not None:
                flags.append(f'--iconv={iconv}')
            rsync_path = getattr(settings, 'rsync_path', None)
            if rsync_path is not None:
                flags.append(f'--rsync-path={rsync_path}')
        return flags


class ServerSettings(ConfigurationSection):
    """
    Server specific common sync settings by server name
    """
    __name__ = 'servers'


class TargetSettings(ConfigurationSection):
    """
    Tree sync targets by name
    """

    __name__ = 'targets'
    __dict_loader_class__ = TargetConfiguration

    @property
    def names(self):
        """
        Get configured target names
        """
        names = []
        for attr in vars(self):
            section = getattr(self, attr)
            if isinstance(section, Configuration):
                continue
            if isinstance(section, self.__dict_loader_class__):
                names.append(attr)
        return names

    def __iter__(self):
        targets = [getattr(self, name) for name in self.names]
        return iter(targets)

    def get_target(self, name):
        """
        Get target by name
        """
        settings = getattr(self, name, None)
        if settings is None:
            raise ValueError(f'Invalid target name {name}')
        return Target(name, settings)


class Configuration(YamlConfiguration):
    """
    Yaml configuration file for 'treesync' CLI
    """
    __default_paths__ = DEFAULT_CONFIGURATION_PATHS
    __section_loaders__ = (
        Defaults,
        ServerSettings,
        TargetSettings,
    )

    def __repr__(self):
        return 'treesync config'

    @property
    def sync_targets(self):
        """
        Get configured sync targets
        """
        targets = []
        # pylint: disable=no-member
        for name in self.targets.names:
            targets.append(self.get_target(name))
        return targets

    def get_target(self, name):
        """
        Get target by name
        """
        # pylint: disable=no-member
        return self.targets.get_target(name)
