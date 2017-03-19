##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    def from_sourcing_files(*args, **kwargs):
        """Creates an instance of EnvironmentModifications that, if executed,
        has the same effect on the environment as sourcing the files passed as
        parameters

        :param \*args: list of files to be sourced
        :rtype: instance of EnvironmentModifications
        """
        env = EnvironmentModifications()

        # Check if the files are actually there
        files = [line.split(' ')[0] for line in args]
        non_existing = [file for file in files if not os.path.isfile(file)]
        if non_existing:
            message = 'trying to source non-existing files\n'
            message += '\n'.join(non_existing)
            raise RuntimeError(message)

        # Relevant kwd parameters and formats
        info = dict(kwargs)
        info.setdefault('shell', '/bin/bash')
        info.setdefault('shell_options', '-c')
        info.setdefault('source_command', 'source')
        info.setdefault('suppress_output', '&> /dev/null')
        info.setdefault('concatenate_on_success', '&&')

        shell = '{shell}'.format(**info)
        shell_options = '{shell_options}'.format(**info)
        source_file = '{source_command} {file} {concatenate_on_success}'

        dump_cmd = "import os, json; print json.dumps(dict(os.environ))"
        dump_environment = 'python -c "%s"' % dump_cmd

        # Construct the command that will be executed
        command = [source_file.format(file=file, **info) for file in args]
        command.append(dump_environment)
        command = ' '.join(command)
        command = [
            shell,
            shell_options,
            command
        ]

        # Try to source all the files,
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, env=os.environ)
        proc.wait()
        if proc.returncode != 0:
            raise RuntimeError('sourcing files returned a non-zero exit code')
        output = ''.join([line for line in proc.stdout])

        # Construct a dictionaries of the environment before and after
        # sourcing the files, so that we can diff them.
        this_environment = dict(os.environ)
        after_source_env = json.loads(output)

        # If we're in python2, convert to str objects instead of unicode
        # like json gives us.  We can't put unicode in os.environ anyway.
        if sys.version_info[0] < 3:
            after_source_env = dict((k.encode('utf-8'), v.encode('utf-8'))
                                    for k, v in after_source_env.items())

        # Filter variables that are not related to sourcing a file
        to_be_filtered = 'SHLVL', '_', 'PWD', 'OLDPWD'
        for d in after_source_env, this_environment:
            for name in to_be_filtered:
                d.pop(name, None)

        # Fill the EnvironmentModifications instance

        # New variables
        new_variables = set(after_source_env) - set(this_environment)
        for x in new_variables:
            env.set(x, after_source_env[x])
        # Variables that have been unset
        unset_variables = set(this_environment) - set(after_source_env)
        for x in unset_variables:
            env.unset(x)
        # Variables that have been modified
        common_variables = set(
            this_environment).intersection(set(after_source_env))
        modified_variables = [x for x in common_variables
                              if this_environment[x] != after_source_env[x]]

        def return_separator_if_any(first_value, second_value):
            separators = ':', ';'
            for separator in separators:
                if separator in first_value and separator in second_value:
                    return separator
            return None

        for x in modified_variables:
            current = this_environment[x]
            modified = after_source_env[x]
            sep = return_separator_if_any(current, modified)
            if sep is None:
                # We just need to set the variable to the new value
                env.set(x, after_source_env[x])
            else:
                current_list = current.split(sep)
                modified_list = modified.split(sep)
                # Paths that have been removed
                remove_list = [
                    ii for ii in current_list if ii not in modified_list]
                # Check that nothing has been added in the middle of vurrent
                # list
                remaining_list = [
                    ii for ii in current_list if ii in modified_list]
                start = modified_list.index(remaining_list[0])
                end = modified_list.index(remaining_list[-1])
                search = sep.join(modified_list[start:end + 1])

                if search not in current:
                    # We just need to set the variable to the new value
                    env.set(x, after_source_env[x])
                    break
                else:
                    try:
                        prepend_list = modified_list[:start]
                    except KeyError:
                        prepend_list = []
                    try:
                        append_list = modified_list[end + 1:]
                    except KeyError:
                        append_list = []

                    for item in remove_list:
                        env.remove_path(x, item)
                    for item in append_list:
                        env.append_path(x, item)
                    for item in prepend_list:
                        env.prepend_path(x, item)

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
