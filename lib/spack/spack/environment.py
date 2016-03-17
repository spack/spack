import os
import os.path
import collections


class NameModifier(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.args = {'name': name}
        self.args.update(kwargs)


class NameValueModifier(object):
    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.args = {'name': name, 'value': value}
        self.args.update(kwargs)


class SetEnv(NameValueModifier):
    def execute(self):
        os.environ[self.name] = str(self.value)


class UnsetEnv(NameModifier):
    def execute(self):
        os.environ.pop(self.name, None)  # Avoid throwing if the variable was not set


class AppendPath(NameValueModifier):
    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        # TODO : Check if this is a valid directory name
        directories.append(os.path.normpath(self.value))
        os.environ[self.name] = ':'.join(directories)


class PrependPath(NameValueModifier):
    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        # TODO : Check if this is a valid directory name
        directories = [os.path.normpath(self.value)] + directories
        os.environ[self.name] = ':'.join(directories)


class RemovePath(NameValueModifier):
    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        directories = [os.path.normpath(x) for x in directories if x != os.path.normpath(self.value)]
        os.environ[self.name] = ':'.join(directories)


class EnvironmentModifications(object):
    """
    Keeps track of requests to modify the current environment.
    """

    def __init__(self, other=None):
        """
        Initializes a new instance, copying commands from other if it is not None

        Args:
            other: another instance of EnvironmentModifications from which (optional)
        """
        self.env_modifications = []
        if other is not None:
            self.extend(other)

    def __iter__(self):
        return iter(self.env_modifications)

    def __len__(self):
        return len(self.env_modifications)

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

    def group_by_name(self):
        """
        Returns a dict of the modifications grouped by variable name

        Returns:
            dict mapping the environment variable name to the modifications to be done on it
        """
        modifications = collections.defaultdict(list)
        for item in self:
            modifications[item.name].append(item)
        return modifications

    def clear(self):
        """
        Clears the current list of modifications
        """
        self.env_modifications.clear()

    def apply_modifications(self):
        """
        Applies the modifications and clears the list
        """
        modifications = self.group_by_name()
        # Apply the modifications to the environment variables one variable at a time
        for name, actions in sorted(modifications.items()):
            for x in actions:
                x.execute()


def concatenate_paths(paths):
    """
    Concatenates an iterable of paths into a  string of column separated paths

    Args:
        paths: iterable of paths

    Returns:
        string
    """
    return ':'.join(str(item) for item in paths)
