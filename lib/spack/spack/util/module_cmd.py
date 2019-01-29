# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains routines related to the module command for accessing and
parsing environment modules.
"""
import subprocess
import re
import os
import llnl.util.tty as tty
from spack.util.executable import which


def get_module_cmd(bashopts=''):
    try:
        return get_module_cmd_from_bash(bashopts)
    except ModuleError:
        # Don't catch the exception this time; we have no other way to do it.
        tty.warn("Could not detect module function from bash."
                 " Trying to detect modulecmd from `which`")
        try:
            return get_module_cmd_from_which()
        except ModuleError:
            raise ModuleError('Spack requires modulecmd or a defined module'
                              ' fucntion. Make sure modulecmd is in your path'
                              ' or the function "module" is defined in your'
                              ' bash environment.')


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


def get_module_cmd_from_bash(bashopts=''):
    # Find how the module function is defined in the environment
    module_func = os.environ.get('BASH_FUNC_module()', None)
    if module_func:
        module_func = os.path.expandvars(module_func)
    else:
        module_func_proc = subprocess.Popen(['{0} typeset -f module | '
                                             'envsubst'.format(bashopts)],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            executable='/bin/bash',
                                            shell=True)
        module_func_proc.wait()
        module_func = module_func_proc.stdout.read()

    # Find the portion of the module function that is evaluated
    try:
        find_exec = re.search(r'.*`(.*(:? bash | sh ).*)`.*', module_func)
        exec_line = find_exec.group(1)
    except BaseException:
        try:
            # This will fail with nested parentheses. TODO: expand regex.
            find_exec = re.search(r'.*\(([^()]*(:? bash | sh )[^()]*)\).*',
                                  module_func)
            exec_line = find_exec.group(1)
        except BaseException:
            raise ModuleError('get_module_cmd cannot '
                              'determine the module command from bash')

    # Create an executable
    args = exec_line.split()
    module_cmd = which(args[0])
    if module_cmd:
        for arg in args[1:]:
            if arg in ('bash', 'sh'):
                module_cmd.add_default_arg('python')
                break
            else:
                module_cmd.add_default_arg(arg)
    else:
        raise ModuleError('Could not create executable based on module'
                          ' function.')

    # Check that the executable works
    module_cmd('list', output=str, error=str, fail_on_error=False)
    if module_cmd.returncode != 0:
        raise ModuleError('get_module_cmd cannot determine the module command'
                          'from bash.')

    return module_cmd


def unload_module(mod):
    """Takes a module name and unloads the module from the environment. It does
    not check whether conflicts arise from the unloaded module"""
    tty.debug("Unloading module: {0}".format(mod))

    modulecmd = get_module_cmd()
    unload_output = modulecmd('unload', mod, output=str, error=str)

    try:
        exec(compile(unload_output, '<string>', 'exec'))
    except Exception:
        tty.debug("Module unload output of {0}:\n{1}\n".format(
            mod, unload_output))
        raise


def load_module(mod):
    """Takes a module name and removes modules until it is possible to
    load that module. It then loads the provided module. Depends on the
    modulecmd implementation of modules used in cray and lmod.
    """
    tty.debug("Loading module: {0}".format(mod))

    # Create an executable of the module command that will output python code
    modulecmd = get_module_cmd()

    # Read the module and remove any conflicting modules
    # We do this without checking that they are already installed
    # for ease of programming because unloading a module that is not
    # loaded does nothing.
    module_content = modulecmd('show', mod, output=str, error=str)
    text = module_content.split()
    try:
        for i, word in enumerate(text):
            if word == 'conflict':
                unload_module(text[i + 1])
    except Exception:
        tty.debug("Module show output of {0}:\n{1}\n".format(
            mod, module_content))
        raise

    # Load the module now that there are no conflicts
    # Some module systems use stdout and some use stderr
    load = modulecmd('load', mod, output=str, error='/dev/null')
    if not load:
        load = modulecmd('load', mod, error=str)

    try:
        exec(compile(load, '<string>', 'exec'))
    except Exception:
        tty.debug("Module load output of {0}:\n{1}\n".format(mod, load))
        raise


def get_path_arg_from_module_line(line):
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
        path_arg = words_and_symbols[-2]
    else:
        path_arg = line.split()[2]
    return path_arg


def get_path_from_module(mod):
    """Inspects a TCL module for entries that indicate the absolute path
    at which the library supported by said module can be found.
    """
    # Create a modulecmd executable
    modulecmd = get_module_cmd()

    # Read the module
    text = modulecmd('show', mod, output=str, error=str).split('\n')

    p = get_path_from_module_contents(text, mod)
    if p and not os.path.exists(p):
        tty.warn("Extracted path from module does not exist:"
                 "\n\tExtracted path: " + p)
    return p


def get_path_from_module_contents(text, module_name):
    tty.debug("Module name: " + module_name)
    pkg_var_prefix = module_name.replace('-', '_').upper()
    components = pkg_var_prefix.split('/')
    # For modules with multiple components like foo/1.0.1, retrieve the package
    # name "foo" from the module name
    if len(components) > 1:
        pkg_var_prefix = components[-2]
    tty.debug("Package directory variable prefix: " + pkg_var_prefix)

    # If it sets the LD_LIBRARY_PATH or CRAY_LD_LIBRARY_PATH, use that
    for line in text:
        pattern = r'\W(CRAY_)?LD_LIBRARY_PATH'
        if re.search(pattern, line):
            path = get_path_arg_from_module_line(line)
            return path[:path.find('/lib')]

    # If it lists its package directory, return that
    for line in text:
        pattern = r'\W{0}_DIR'.format(pkg_var_prefix)
        if re.search(pattern, line):
            return get_path_arg_from_module_line(line)

    # If it lists a -rpath instruction, use that
    for line in text:
        rpath = line.find('-rpath/')
        if rpath >= 0:
            return line[rpath + 6:line.find('/lib')]

    # If it lists a -L instruction, use that
    for line in text:
        lib_paths = line.find('-L/')
        if lib_paths >= 0:
            return line[lib_paths + 2:line.find('/lib')]

    # If it sets the PATH, use it
    for line in text:
        pattern = r'\WPATH'
        if re.search(pattern, line):
            path = get_path_arg_from_module_line(line)
            return path[:path.find('/bin')]

    # Unable to find module path
    return None


class ModuleError(Exception):
    """Raised the the module_cmd utility to indicate errors."""
