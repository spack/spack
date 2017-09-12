##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import collections
import inspect
import json
import os
import sys
import os.path
import subprocess


class NameModifier(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.args = {'name': name}
        self.args.update(kwargs)

    def update_args(self, **kwargs):
        self.__dict__.update(kwargs)
        self.args.update(kwargs)


class NameValueModifier(object):

    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.separator = kwargs.get('separator', ':')
        self.args = {'name': name, 'value': value, 'separator': self.separator}
        self.args.update(kwargs)

    def update_args(self, **kwargs):
        self.__dict__.update(kwargs)
        self.args.update(kwargs)


class SetEnv(NameValueModifier):

    def execute(self):
        os.environ[self.name] = str(self.value)


class AppendFlagsEnv(NameValueModifier):

    def execute(self):
        if self.name in os.environ and os.environ[self.name]:
            os.environ[self.name] += self.separator + str(self.value)
        else:
            os.environ[self.name] = str(self.value)


class UnsetEnv(NameModifier):

    def execute(self):
        # Avoid throwing if the variable was not set
        os.environ.pop(self.name, None)


class SetPath(NameValueModifier):

    def execute(self):
        string_path = concatenate_paths(self.value, separator=self.separator)
        os.environ[self.name] = string_path


class AppendPath(NameValueModifier):

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(
            self.separator) if environment_value else []
        directories.append(os.path.normpath(self.value))
        os.environ[self.name] = self.separator.join(directories)


class PrependPath(NameValueModifier):

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(
            self.separator) if environment_value else []
        directories = [os.path.normpath(self.value)] + directories
        os.environ[self.name] = self.separator.join(directories)


class RemovePath(NameValueModifier):

    def execute(self):
        environment_value = os.environ.get(self.name, '')
        directories = environment_value.split(
            self.separator) if environment_value else []
        directories = [os.path.normpath(x) for x in directories
                       if x != os.path.normpath(self.value)]
        os.environ[self.name] = self.separator.join(directories)


class EnvironmentModifications(object):

    """
    Keeps track of requests to modify the current environment.

    Each call to a method to modify the environment stores the extra
    information on the caller in the request:
    - 'filename' : filename of the module where the caller is defined
    - 'lineno': line number where the request occurred
    - 'context' : line of code that issued the request that failed
    """

    def __init__(self, other=None):
        """
        Initializes a new instance, copying commands from other if not None

        Args:
            other: another instance of EnvironmentModifications (optional)
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
            raise TypeError(
                'other must be an instance of EnvironmentModifications')

    def _get_outside_caller_attributes(self):
        stack = inspect.stack()
        try:
            _, filename, lineno, _, context, index = stack[2]
            context = context[index].strip()
        except Exception:
            filename = 'unknown file'
            lineno = 'unknown line'
            context = 'unknown context'
        args = {'filename': filename, 'lineno': lineno, 'context': context}
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

    def append_flags(self, name, value, sep=' ', **kwargs):
        """
        Stores in the current object a request to append to an env variable

        Args:
            name: name of the environment variable to be appended to
            value: value to append to the environment variable
        Appends with spaces separating different additions to the variable
        """
        kwargs.update(self._get_outside_caller_attributes())
        kwargs.update({'separator': sep})
        item = AppendFlagsEnv(name, value, **kwargs)
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
        Stores in the current object a request to remove a path from a path
        list

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
            dict mapping the environment variable name to the modifications to
            be done on it
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
        # Apply modifications one variable at a time
        for name, actions in sorted(modifications.items()):
            for x in actions:
                x.execute()

    @staticmethod
    def from_sourcing_file(filename, *args, **kwargs):
        """Returns modifications that would be made by sourcing a file.

        Parameters:
            filename (str): The file to source
            *args (list of str): Arguments to pass on the command line

        Keyword Arguments:
            shell (str): The shell to use (default: ``bash``)
            shell_options (str): Options passed to the shell (default: ``-c``)
            source_command (str): The command to run (default: ``source``)
            suppress_output (str): Redirect used to suppress output of command
                (default: ``&> /dev/null``)
            concatenate_on_success (str): Operator used to execute a command
                only when the previous command succeeds (default: ``&&``)

        Returns:
            EnvironmentModifications: an object that, if executed, has
                the same effect on the environment as sourcing the file
        """
        # Check if the file actually exists
        if not os.path.isfile(filename):
            msg = 'Trying to source non-existing file: {0}'.format(filename)
            raise RuntimeError(msg)

        # Kwargs parsing and default values
        shell                  = kwargs.get('shell', '/bin/bash')
        shell_options          = kwargs.get('shell_options', '-c')
        source_command         = kwargs.get('source_command', 'source')
        suppress_output        = kwargs.get('suppress_output', '&> /dev/null')
        concatenate_on_success = kwargs.get('concatenate_on_success', '&&')

        source_file = [source_command, filename]
        source_file.extend(args)
        source_file = ' '.join(source_file)

        dump_cmd = 'import os, json; print(json.dumps(dict(os.environ)))'
        dump_environment = 'python -c "{0}"'.format(dump_cmd)

        # Construct the command that will be executed
        command = [
            shell,
            shell_options,
            ' '.join([
                source_file, suppress_output,
                concatenate_on_success, dump_environment,
            ]),
        ]

        # Try to source the file
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, env=os.environ)
        proc.wait()

        if proc.returncode != 0:
            msg = 'Sourcing file {0} returned a non-zero exit code'.format(
                filename)
            raise RuntimeError(msg)

        output = ''.join([line.decode('utf-8') for line in proc.stdout])

        # Construct dictionaries of the environment before and after
        # sourcing the file, so that we can diff them.
        env_before = dict(os.environ)
        env_after = json.loads(output)

        # If we're in python2, convert to str objects instead of unicode
        # like json gives us.  We can't put unicode in os.environ anyway.
        if sys.version_info[0] < 3:
            env_after = dict((k.encode('utf-8'), v.encode('utf-8'))
                             for k, v in env_after.items())

        # Filter variables that are not related to sourcing a file
        to_be_filtered = 'SHLVL', '_', 'PWD', 'OLDPWD', 'PS2'
        for d in env_after, env_before:
            for name in to_be_filtered:
                d.pop(name, None)

        # Fill the EnvironmentModifications instance
        env = EnvironmentModifications()

        # New variables
        new_variables = set(env_after) - set(env_before)
        # Variables that have been unset
        unset_variables = set(env_before) - set(env_after)
        # Variables that have been modified
        common_variables = set(
            env_before).intersection(set(env_after))
        modified_variables = [x for x in common_variables
                              if env_before[x] != env_after[x]]

        def return_separator_if_any(*args):
            separators = ':', ';'
            for separator in separators:
                for arg in args:
                    if separator in arg:
                        return separator
            return None

        # Add variables to env.
        # Assume that variables with 'PATH' in the name or that contain
        # separators like ':' or ';' are more likely to be paths
        for x in new_variables:
            sep = return_separator_if_any(env_after[x])
            if sep:
                env.prepend_path(x, env_after[x], separator=sep)
            elif 'PATH' in x:
                env.prepend_path(x, env_after[x])
            else:
                # We just need to set the variable to the new value
                env.set(x, env_after[x])

        for x in unset_variables:
            env.unset(x)

        for x in modified_variables:
            before = env_before[x]
            after = env_after[x]
            sep = return_separator_if_any(before, after)
            if sep:
                before_list = before.split(sep)
                after_list = after.split(sep)

                # Filter out empty strings
                before_list = list(filter(None, before_list))
                after_list = list(filter(None, after_list))

                # Paths that have been removed
                remove_list = [
                    ii for ii in before_list if ii not in after_list]
                # Check that nothing has been added in the middle of
                # before_list
                remaining_list = [
                    ii for ii in before_list if ii in after_list]
                try:
                    start = after_list.index(remaining_list[0])
                    end = after_list.index(remaining_list[-1])
                    search = sep.join(after_list[start:end + 1])
                except IndexError:
                    env.prepend_path(x, env_after[x])

                if search not in before:
                    # We just need to set the variable to the new value
                    env.prepend_path(x, env_after[x])
                else:
                    try:
                        prepend_list = after_list[:start]
                    except KeyError:
                        prepend_list = []
                    try:
                        append_list = after_list[end + 1:]
                    except KeyError:
                        append_list = []

                    for item in remove_list:
                        env.remove_path(x, item)
                    for item in append_list:
                        env.append_path(x, item)
                    for item in prepend_list:
                        env.prepend_path(x, item)
            else:
                # We just need to set the variable to the new value
                env.set(x, env_after[x])

        return env


def concatenate_paths(paths, separator=':'):
    """
    Concatenates an iterable of paths into a string of paths separated by
    separator, defaulting to colon

    Args:
        paths: iterable of paths
        separator: the separator to use, default ':'

    Returns:
        string
    """
    return separator.join(str(item) for item in paths)


def set_or_unset_not_first(variable, changes, errstream):
    """
    Check if we are going to set or unset something after other modifications
    have already been requested
    """
    indexes = [ii for ii, item in enumerate(changes)
               if ii != 0 and type(item) in [SetEnv, UnsetEnv]]
    if indexes:
        good = '\t    \t{context} at {filename}:{lineno}'
        nogood = '\t--->\t{context} at {filename}:{lineno}'
        message = "Suspicious requests to set or unset '{var}' found"
        errstream(message.format(var=variable))
        for ii, item in enumerate(changes):
            print_format = nogood if ii in indexes else good
            errstream(print_format.format(**item.args))


def validate(env, errstream):
    """
    Validates the environment modifications to check for the presence of
    suspicious patterns. Prompts a warning for everything that was found

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
    Generator that filters out any change to environment variables present in
    the input list

    Args:
        env: list of environment modifications
        variables: list of variable names to be filtered

    Yields:
        items in env if they are not in variables
    """
    for item in env:
        if item.name not in variables:
            yield item
