import os
import os.path
import collections


class SetEnv(object):
    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        os.environ[self.name] = str(self.value)


class UnsetEnv(object):
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        os.environ.pop(self.name, None)  # Avoid throwing if the variable was not set


class AppendPath(object):
    def __init__(self, name, path, **kwargs):
        self.name = name
        self.path = path
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        # TODO : Check if this is a valid directory name
        directories.append(os.path.normpath(self.path))
        os.environ[self.name] = ':'.join(directories)


class PrependPath(object):
    def __init__(self, name, path, **kwargs):
        self.name = name
        self.path = path
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        # TODO : Check if this is a valid directory name
        directories = [os.path.normpath(self.path)] + directories
        os.environ[self.name] = ':'.join(directories)


class RemovePath(object):
    def __init__(self, name, path, **kwargs):
        self.name = name
        self.path = path
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        directories = [os.path.normpath(x) for x in directories if x != os.path.normpath(self.path)]
        os.environ[self.name] = ':'.join(directories)


class EnvironmentModifications(object):
    """
    Keeps track of requests to modify the current environment
    """

    def __init__(self, other=None):
        self.env_modifications = []
        if other is not None:
            self._check_other(other)
            self.env_modifications.extend(other.env_modifications)

    def __iter__(self):
        return iter(self.env_modifications)

    def extend(self, other):
        self._check_other(other)
        self.env_modifications.extend(other.env_modifications)

    @staticmethod
    def _check_other(other):
        if not isinstance(other, EnvironmentModifications):
            raise TypeError('other must be an instance of EnvironmentModifications')

    def set_env(self, name, value, **kwargs):
        """
        Stores in the current object a request to set an environment variable

        Args:
            name: name of the environment variable to be set
            value: value of the environment variable
        """
        item = SetEnv(name, value, **kwargs)
        self.env_modifications.append(item)

    def unset_env(self, name, **kwargs):
        """
        Stores in the current object a request to unset an environment variable

        Args:
            name: name of the environment variable to be set
        """
        item = UnsetEnv(name, **kwargs)
        self.env_modifications.append(item)

    def append_path(self, name, path, **kwargs):
        """
        Stores in the current object a request to append a path to a path list

        Args:
            name: name of the path list in the environment
            path: path to be appended
        """
        item = AppendPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def prepend_path(self, name, path, **kwargs):
        """
        Same as `append_path`, but the path is pre-pended

        Args:
            name: name of the path list in the environment
            path: path to be pre-pended
        """
        item = PrependPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def remove_path(self, name, path, **kwargs):
        """
        Stores in the current object a request to remove a path from a path list

        Args:
            name: name of the path list in the environment
            path: path to be removed
        """
        item = RemovePath(name, path, **kwargs)
        self.env_modifications.append(item)


def concatenate_paths(paths):
    return ':'.join(str(item) for item in paths)

def validate_environment_modifications(env):
    modifications = collections.defaultdict(list)
    for item in env:
        modifications[item.name].append(item)
    # TODO : once we organized the modifications into a dictionary that maps an environment variable
    # TODO : to a list of action to be done on it, we may easily spot inconsistencies and warn the user if
    # TODO : something suspicious is happening
    return modifications


def apply_environment_modifications(env):
    """
    Modifies the current environment according to the request in env

    Args:
        env: object storing modifications to the environment
    """
    modifications = validate_environment_modifications(env)

    # Cycle over the environment variables that will be modified
    for variable, actions in modifications.items():
        # Execute all the actions in the order they were issued
        for x in actions:
            x.execute()
