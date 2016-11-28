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

import os
import subprocess
import re

from spack.util.executable import Executable, which

# Cache of the modulecmd executable
_modulecmd_exe = None


def get_modulecmd():
    global _modulecmd_exe
    if _modulecmd_exe:
        return _modulecmd_exe

    # Try to find the way to call modulecmd by looking into the definition
    # of the shell module function.
    result = _get_modulecmd_from_shell_function()

    if result:
        _modulecmd_exe = result
    else:
        _modulecmd_exe = which('modulecmd', required=True)

    _modulecmd_exe.add_default_arg('python')

    return _modulecmd_exe


def _get_modulecmd_from_shell_function():
    # Get the definition of the module function.
    type_cmd = subprocess.Popen(
        [os.environ['SHELL'], '-ic', 'type module'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    std, err = type_cmd.communicate()

    if type_cmd.returncode == 0:
        # We assume that the user's shell is bash. We also assume that the
        # module function is declared as a single eval command.
        match = re.search(r'module\s*\(\s*\)\s*\{\s*eval\s+'
                          r'`(.*)\s+bash\s+\$\*`'
                          r'\s+\}\s*$',
                          std)

        # Expand the variables that appear in the module function definition.
        echo_cmd = subprocess.Popen(
            [os.environ['SHELL'],
             '-ic',
             'echo -n %s' % match.group(1)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        std, err = echo_cmd.communicate()

        result = Executable(std)

        # Try to run the executable.
        result('python', 'list', output=str, error=str, fail_on_error=False)

        if result.returncode == 0:
            return result
