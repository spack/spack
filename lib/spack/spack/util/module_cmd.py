##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
"""
This module contains routines related to the module command for accessing and
parsing environment modules.
"""
import re
import os
import shlex

import llnl.util.tty as tty
from spack.util.executable import which


def get_module_cmd():
    try:
        result = get_module_cmd_from_bash()
    except ModuleError:
        # Don't catch the exception this time; we have no other way to do it.
        tty.warn("Could not detect module function from bash."
                 " Trying to detect modulecmd from `which`")
        try:
            result = get_module_cmd_from_which()
        except ModuleError:
            result = None

    if result is None:
        raise ModuleError('Spack requires modulecmd or a defined module '
                          'function. Make sure modulecmd is in your path '
                          'or the function "module" is defined in your '
                          'bash environment.')

    if re.match(r'^Modules Release Tcl 3\.',
                result(error=str)) is not None:
        result.post_processor = old_tcl_postprocessor

    return result


def get_module_cmd_from_which():
    module_cmd = which('modulecmd')
    if not module_cmd:
        raise ModuleError('`which` did not find any modulecmd executable')
    module_cmd.add_default_arg('python')

    # Check that the executable works
    module_cmd('list', output=str, error=str, fail_on_error=False)
    if module_cmd.returncode != 0:
        raise ModuleError('get_module_cmd cannot determine the module command')

    return module_cmd


def get_module_cmd_from_bash():
    # Take the first bash from the $PATH
    bash = which('bash')
    if bash is None:
        raise ModuleError('Bash executable not found.')

    # We assume that if the shell function 'module' is available at all, it
    # should be available at least in the case of the interactive login shell.
    bash.add_default_arg('-l')
    bash.add_default_arg('-i')

    # We will call bash to run the scripts from the command line.
    bash.add_default_arg('-c')

    # Depending on the version, Bash stores shell functions as environment
    # variables under different names (e.g. BASH_FUNC_module(),
    # BASH_FUNC_module%%). Thus, we don't check the variables but call
    # 'typeset -f module' to get the definition of the function.
    module_func_str = bash('typeset -f module',
                           output=str,
                           error=os.devnull,
                           fail_on_error=False)

    if bash.returncode != 0:
        raise ModuleError('Bash function \'module\' is not defined.')

    # Bash initialization scripts might define the function 'module' using
    # shell variables that are not exported. Thus, we export everything.
    bash_init_vars_str = bash('export $(compgen -v); env --null',
                              output=str,
                              error=os.devnull,
                              fail_on_error=False)

    bash_init_vars_dict = {}
    if bash_init_vars_str:
        for var_record in bash_init_vars_str.strip('\0').split('\0'):
            name_value = var_record.split('=', 1)
            if len(name_value) == 2:
                bash_init_vars_dict[name_value[0]] = name_value[1]

    # Expand variables in the function definition.
    env_bu = os.environ.copy()
    try:
        os.environ.clear()
        os.environ.update(bash_init_vars_dict)
        module_func_str = os.path.expandvars(module_func_str)
        module_func_str = os.path.expanduser(module_func_str)
    except BaseException:
        raise ModuleError('Failed to expand variables in the definition of '
                          'bash function \'module\'.')
    finally:
        os.environ.clear()
        os.environ.update(env_bu)

    # Find the portion of the module function that is evaluated
    try:
        find_exec = re.search(r'.*`(.*(:? bash | sh ).*)`.*', module_func_str)
        exec_line = find_exec.group(1)
    except BaseException:
        try:
            # This will fail with nested parentheses. TODO: expand regex.
            find_exec = re.search(r'.*\(([^()]*(:? bash | sh )[^()]*)\).*',
                                  module_func_str)
            exec_line = find_exec.group(1)
        except BaseException:
            raise ModuleError('Failed to determine the module command from '
                              'bash.')

    # Create an executable
    args = shlex.split(exec_line)
    module_cmd = which(args[0])
    if module_cmd:
        for arg in args[1:]:
            if arg in ('bash', 'sh'):
                module_cmd.add_default_arg('python')
                break
            else:
                module_cmd.add_default_arg(arg)
    else:
        raise ModuleError('Failed to create executable based on shell '
                          'function \'module\'.')

    # Check that the executable works
    module_cmd('list', output=str, error=str, fail_on_error=False)
    if module_cmd.returncode != 0:
        raise ModuleError('The module command that was determined from bash '
                          'doesn\'t work as expected.')

    return module_cmd


def load_module(mod):
    """Takes a module name and removes modules until it is possible to
    load that module. It then loads the provided module. Depends on the
    modulecmd implementation of modules used in cray and lmod.
    """
    # Create an executable of the module command that will output python code
    modulecmd = get_module_cmd()

    # Read the module and remove any conflicting modules
    # We do this without checking that they are already installed
    # for ease of programming because unloading a module that is not
    # loaded does nothing.
    text = modulecmd('show', mod, output=str, error=str).split()
    for i, word in enumerate(text):
        if word == 'conflict':
            exec(compile(modulecmd('unload', text[i + 1], output=str,
                                   error=str), '<string>', 'exec'))
    # Load the module now that there are no conflicts
    load = modulecmd('load', mod, output=str, error=str)
    exec(compile(load, '<string>', 'exec'))


def get_argument_from_module_line(line):
    if '(' in line and ')' in line:
        # Determine which lua quote symbol is being used for the argument
        comma_index = line.index(',')
        cline = line[comma_index:]
        try:
            quote_index = min(cline.find(q) for q in ['"', "'"] if q in cline)
            lua_quote = cline[quote_index]
        except ValueError:
            # Change error text to describe what is going on.
            raise ValueError("No lua quote symbol found in lmod module line.")
        words_and_symbols = line.split(lua_quote)
        return words_and_symbols[-2]
    else:
        return line.split()[2]


def get_path_from_module(mod):
    """Inspects a TCL module for entries that indicate the absolute path
    at which the library supported by said module can be found.
    """
    # Create a modulecmd executable
    modulecmd = get_module_cmd()

    # Read the module
    text = modulecmd('show', mod, output=str, error=str).split('\n')

    # If it sets the LD_LIBRARY_PATH or CRAY_LD_LIBRARY_PATH, use that
    for line in text:
        if line.find('LD_LIBRARY_PATH') >= 0:
            path = get_argument_from_module_line(line)
            return path[:path.find('/lib')]

    # If it lists its package directory, return that
    for line in text:
        if line.find(mod.upper() + '_DIR') >= 0:
            return get_argument_from_module_line(line)

    # If it lists a -rpath instruction, use that
    for line in text:
        rpath = line.find('-rpath/')
        if rpath >= 0:
            return line[rpath + 6:line.find('/lib')]

    # If it lists a -L instruction, use that
    for line in text:
        L = line.find('-L/')
        if L >= 0:
            return line[L + 2:line.find('/lib')]

    # If it sets the PATH, use it
    for line in text:
        if line.find('PATH') >= 0:
            path = get_argument_from_module_line(line)
            return path[:path.find('/bin')]

    # Unable to find module path
    return None


def old_tcl_postprocessor(out, err):
    """Fixes incorrect python scripts generated by old versions of
    Environment Modules Tcl.
    """
    if out:
        out = re.sub(r"""^exec\s+["']([\w/]*modulescript_[0-9_]+)["']$""",
                     r"""exec(open('\1').read())""", out)
    return out, err


class ModuleError(Exception):
    """Raised the the module_cmd utility to indicate errors."""
