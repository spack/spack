##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import contextlib
import inspect
import json
import os
import re
import sys
import os.path
import subprocess

import llnl.util.tty as tty

from llnl.util.lang import dedupe


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
    """Keeps track of requests to modify the current environment.

    Each call to a method to modify the environment stores the extra
    information on the caller in the request:

        * 'filename' : filename of the module where the caller is defined
        * 'lineno': line number where the request occurred
        * 'context' : line of code that issued the request that failed
    """

    def __init__(self, other=None):
        """Initializes a new instance, copying commands from 'other'
        if it is not None.

        Args:
            other (EnvironmentModifications): list of environment modifications
                to be extended (optional)
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
        """Stores a request to set an environment variable.

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
        """Stores a request to unset an environment variable.

        Args:
            name: name of the environment variable to be set
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = UnsetEnv(name, **kwargs)
        self.env_modifications.append(item)

    def set_path(self, name, elements, **kwargs):
        """Stores a request to set a path generated from a list.

        Args:
            name: name o the environment variable to be set.
            elements: elements of the path to set.
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = SetPath(name, elements, **kwargs)
        self.env_modifications.append(item)

    def append_path(self, name, path, **kwargs):
        """Stores a request to append a path to a path list.

        Args:
            name: name of the path list in the environment
            path: path to be appended
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = AppendPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def prepend_path(self, name, path, **kwargs):
        """Same as `append_path`, but the path is pre-pended.

        Args:
            name: name of the path list in the environment
            path: path to be pre-pended
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = PrependPath(name, path, **kwargs)
        self.env_modifications.append(item)

    def remove_path(self, name, path, **kwargs):
        """Stores a request to remove a path from a path list.

        Args:
            name: name of the path list in the environment
            path: path to be removed
        """
        kwargs.update(self._get_outside_caller_attributes())
        item = RemovePath(name, path, **kwargs)
        self.env_modifications.append(item)

    def group_by_name(self):
        """Returns a dict of the modifications grouped by variable name.

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
        """Applies the modifications and clears the list."""
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
            blacklist ([str or re]): Ignore any modifications of these
                variables (default: [])
            whitelist ([str or re]): Always respect modifications of these
                variables (default: []). Has precedence over blacklist.
            clean (bool): In addition to removing empty entries,
                also remove duplicate entries (default: False).

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
        blacklist              = kwargs.get('blacklist', [])
        whitelist              = kwargs.get('whitelist', [])
        clean                  = kwargs.get('clean', False)

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

        # Other variables unrelated to sourcing a file
        blacklist.extend(['SHLVL', '_', 'PWD', 'OLDPWD', 'PS2'])

        def set_intersection(fullset, *args):
            # A set intersection using string literals and regexs
            meta = '[' + re.escape('[$()*?[]^{|}') + ']'
            subset = fullset & set(args)   # As literal
            for name in args:
                if re.search(meta, name):
                    pattern = re.compile(name)
                    for k in fullset:
                        if re.match(pattern, k):
                            subset.add(k)
            return subset

        for d in env_after, env_before:
            # Retain (whitelist) has priority over prune (blacklist)
            prune = set_intersection(set(d), *blacklist)
            prune -= set_intersection(prune, *whitelist)
            for k in prune:
                d.pop(k, None)

        # Fill the EnvironmentModifications instance
        env = EnvironmentModifications()

        # New variables
        new_variables = list(set(env_after) - set(env_before))
        # Variables that have been unset
        unset_variables = list(set(env_before) - set(env_after))
        # Variables that have been modified
        common_variables = set(env_before).intersection(set(env_after))

        modified_variables = [x for x in common_variables
                              if env_before[x] != env_after[x]]

        # Consistent output order - looks nicer, easier comparison...
        new_variables.sort()
        unset_variables.sort()
        modified_variables.sort()

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

                # Remove duplicate entries (worse matching, bloats env)
                if clean:
                    before_list = list(dedupe(before_list))
                    after_list = list(dedupe(after_list))
                    # The reassembled cleaned entries
                    before = sep.join(before_list)
                    after = sep.join(after_list)

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
                    env.prepend_path(x, after)

                if search not in before:
                    # We just need to set the variable to the new value
                    env.prepend_path(x, after)
                else:
                    try:
                        prepend_list = after_list[:start]
                        prepend_list.reverse()  # Preserve order after prepend
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
                env.set(x, after)

        return env


def concatenate_paths(paths, separator=':'):
    """Concatenates an iterable of paths into a string of paths separated by
    separator, defaulting to colon.

    Args:
        paths: iterable of paths
        separator: the separator to use, default ':'

    Returns:
        string
    """
    return separator.join(str(item) for item in paths)


def set_or_unset_not_first(variable, changes, errstream):
    """Check if we are going to set or unset something after other
    modifications have already been requested.
    """
    indexes = [ii for ii, item in enumerate(changes)
               if ii != 0 and
               not item.args.get('force', False) and
               type(item) in [SetEnv, UnsetEnv]]
    if indexes:
        good = '\t    \t{context} at {filename}:{lineno}'
        nogood = '\t--->\t{context} at {filename}:{lineno}'
        message = "Suspicious requests to set or unset '{var}' found"
        errstream(message.format(var=variable))
        for ii, item in enumerate(changes):
            print_format = nogood if ii in indexes else good
            errstream(print_format.format(**item.args))


def validate(env, errstream):
    """Validates the environment modifications to check for the presence of
    suspicious patterns. Prompts a warning for everything that was found.

    Current checks:
    - set or unset variables after other changes on the same variable

    Args:
        env: list of environment modifications
    """
    modifications = env.group_by_name()
    for variable, list_of_changes in sorted(modifications.items()):
        set_or_unset_not_first(variable, list_of_changes, errstream)


def filter_environment_blacklist(env, variables):
    """Generator that filters out any change to environment variables present in
    the input list.

    Args:
        env: list of environment modifications
        variables: list of variable names to be filtered

    Returns:
        items in env if they are not in variables
    """
    for item in env:
        if item.name not in variables:
            yield item


def inspect_path(root, inspections, exclude=None):
    """Inspects ``root`` to search for the subdirectories in ``inspections``.
    Adds every path found to a list of prepend-path commands and returns it.

    Args:
        root (str): absolute path where to search for subdirectories

        inspections (dict): maps relative paths to a list of environment
            variables that will be modified if the path exists. The
            modifications are not performed immediately, but stored in a
            command object that is returned to client

        exclude (callable): optional callable. If present it must accept an
            absolute path and return True if it should be excluded from the
            inspection

    Examples:

    The following lines execute an inspection in ``/usr`` to search for
    ``/usr/include`` and ``/usr/lib64``. If found we want to prepend
    ``/usr/include`` to ``CPATH`` and ``/usr/lib64`` to ``MY_LIB64_PATH``.

        .. code-block:: python

            # Set up the dictionary containing the inspection
            inspections = {
                'include': ['CPATH'],
                'lib64': ['MY_LIB64_PATH']
            }

            # Get back the list of command needed to modify the environment
            env = inspect_path('/usr', inspections)

            # Eventually execute the commands
            env.apply_modifications()

    Returns:
        instance of EnvironmentModifications containing the requested
        modifications
    """
    if exclude is None:
        exclude = lambda x: False

    env = EnvironmentModifications()
    # Inspect the prefix to check for the existence of common directories
    for relative_path, variables in inspections.items():
        expected = os.path.join(root, relative_path)

        if os.path.isdir(expected) and not exclude(expected):
            for variable in variables:
                env.prepend_path(variable, expected)

    return env


@contextlib.contextmanager
def preserve_environment(*variables):
    """Ensures that the value of the environment variables passed as
    arguments is the same before entering to the context manager and after
    exiting it.

    Variables that are unset before entering the context manager will be
    explicitly unset on exit.

    Args:
        variables (list of str): list of environment variables to be preserved
    """
    cache = {}
    for var in variables:
        # The environment variable to be preserved might not be there.
        # In that case store None as a placeholder.
        cache[var] = os.environ.get(var, None)

    yield

    for var in variables:
        value = cache[var]
        msg = '[PRESERVE_ENVIRONMENT]'
        if value is not None:
            # Print a debug statement if the value changed
            if var not in os.environ:
                msg += ' {0} was unset, will be reset to "{1}"'
                tty.debug(msg.format(var, value))
            elif os.environ[var] != value:
                msg += ' {0} was set to "{1}", will be reset to "{2}"'
                tty.debug(msg.format(var, os.environ[var], value))
            os.environ[var] = value
        elif var in os.environ:
            msg += ' {0} was set to "{1}", will be unset'
            tty.debug(msg.format(var, os.environ[var]))
            del os.environ[var]
