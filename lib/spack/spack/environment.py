import os
import os.path
import collections
import inspect


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


class SetPath(NameValueModifier):
    def execute(self):
        string_path = concatenate_paths(self.value)
        os.environ[self.name] = string_path


class AppendPath(NameValueModifier):
    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
        directories.append(os.path.normpath(self.value))
        os.environ[self.name] = ':'.join(directories)


class PrependPath(NameValueModifier):
    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(':') if environment_value else []
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

    Each call to a method to modify the environment stores the extra information on the caller in the request:
    - 'filename' : filename of the module where the caller is defined
    - 'lineno': line number where the request occurred
    - 'context' : line of code that issued the request that failed
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

    def _get_outside_caller_attributes(self):
        stack = inspect.stack()
        try:
            _, filename, lineno, _, context, index = stack[2]
            context = context[index].strip()
        except Exception:
            filename, lineno, context = 'unknown file', 'unknown line', 'unknown context'
        args = {
            'filename': filename,
            'lineno': lineno,
            'context': context
        }
        return args

    def set(self, name, value, **kwargs):
        """
        Stores in the current object a request to set an environment variable

        Args:
            name: name of the environment variable to be set
            value: value of the environment variable
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = SetEnv(name, value, **kwargs)
        self.env_modifications.append(item)

    def unset(self, name, **kwargs):
        """
        Stores in the current object a request to unset an environment variable

        Args:
            name: name of the environment variable to be set
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = UnsetEnv(name, **kwargs)
        self.env_modifications.append(item)

    def set_path(self, name, elts, **kwargs):
        """
        Stores a request to set a path generated from a list.

        Args:
            name: name o the environment variable to be set.
            elts: elements of the path to set.
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = SetPath(name, elts, **kwargs)
        self.env_modifications.append(item)

    def append_path(self, name, path, **kwargs):
        """
        Stores in the current object a request to append a path to a path list

        Args:
            name: name of the path list in the environment
            path: path to be appended
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = AppendPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def prepend_path(self, name, path, **kwargs):
        """
        Same as `append_path`, but the path is pre-pended

        Args:
            name: name of the path list in the environment
            path: path to be pre-pended
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = PrependPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def remove_path(self, name, path, **kwargs):
        """
        Stores in the current object a request to remove a path from a path list

        Args:
            name: name of the path list in the environment
            path: path to be removed
        """
        kwargs.update(self._get_outside_caller_attributes())
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


def set_or_unset_not_first(variable, changes, errstream):
    """
    Check if we are going to set or unset something after other modifications have already been requested
    """
    indexes = [ii for ii, item in enumerate(changes) if ii != 0 and type(item) in [SetEnv, UnsetEnv]]
    if indexes:
        good = '\t    \t{context} at {filename}:{lineno}'
        nogood = '\t--->\t{context} at {filename}:{lineno}'
        errstream('Suspicious requests to set or unset the variable \'{var}\' found'.format(var=variable))
        for ii, item in enumerate(changes):
            print_format = nogood if ii in indexes else good
            errstream(print_format.format(**item.args))


def validate(env, errstream):
    """
    Validates the environment modifications to check for the presence of suspicious patterns. Prompts a warning for
    everything that was found

    Current checks:
    - set or unset variables after other changes on the same variable

    Args:
        env: list of environment modifications
    """
    modifications = env.group_by_name()
    for variable, list_of_changes in sorted(modifications.items()):
        set_or_unset_not_first(variable, list_of_changes, errstream)


def filter_environment_blacklist(env, variables):
    """
    Generator that filters out any change to environment variables present in the input list

    Args:
        env: list of environment modifications
        variables: list of variable names to be filtered

    Yields:
        items in env if they are not in variables
    """
    for item in env:
        if item.name not in variables:
            yield item
