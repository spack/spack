# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains routines related to the module command for accessing and
parsing environment modules.
"""
import subprocess
import os
import json
import re

import llnl.util.tty as tty

# This list is not exhaustive. Currently we only use load and unload
# If we need another option that changes the environment, add it here.
module_change_commands = ['load', 'swap', 'unload', 'purge', 'use', 'unuse']
py_cmd = "'import os\nimport json\nprint(json.dumps(dict(os.environ)))'"

# This is just to enable testing. I hate it but we can't find a better way
_test_mode = False


def module(*args):
    module_cmd = 'module ' + ' '.join(args) + ' 2>&1'
    if _test_mode:
        tty.warn('module function operating in test mode')
        module_cmd = ". %s 2>&1" % args[1]
    if args[0] in module_change_commands:
        # Do the module manipulation, then output the environment in JSON
        # and read the JSON back in the parent process to update os.environ
        module_cmd += ' >/dev/null; python -c %s' % py_cmd
        module_p  = subprocess.Popen(module_cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     shell=True,
                                     executable="/bin/bash")

        # Cray modules spit out warnings that we cannot supress.
        # This hack skips to the last output (the environment)
        env_output = str(module_p.communicate()[0].decode())
        env = env_output.strip().split('\n')[-1]

        # Update os.environ with new dict
        env_dict = json.loads(env)
        os.environ.clear()
        os.environ.update(env_dict)
    else:
        # Simply execute commands that don't change state and return output
        module_p = subprocess.Popen(module_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    shell=True,
                                    executable="/bin/bash")
        # Decode and str to return a string object in both python 2 and 3
        return str(module_p.communicate()[0].decode())


def load_module(mod):
    """Takes a module name and removes modules until it is possible to
    load that module. It then loads the provided module. Depends on the
    modulecmd implementation of modules used in cray and lmod.
    """
    # Read the module and remove any conflicting modules
    # We do this without checking that they are already installed
    # for ease of programming because unloading a module that is not
    # loaded does nothing.
    text = module('show', mod).split()
    for i, word in enumerate(text):
        if word == 'conflict':
            module('unload', text[i + 1])

    # Load the module now that there are no conflicts
    # Some module systems use stdout and some use stderr
    module('load', mod)


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
    # Read the module
    text = module('show', mod).split('\n')

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
