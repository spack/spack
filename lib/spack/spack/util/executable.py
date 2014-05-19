##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import sys
import re
import subprocess

import llnl.util.tty as tty
from spack.error import SpackError


class Executable(object):
    """Class representing a program that can be run on the command line."""
    def __init__(self, name):
        self.exe = name.split(' ')
        self.returncode = None

    def add_default_arg(self, arg):
        self.exe.append(arg)


    @property
    def command(self):
        return ' '.join(self.exe)


    def __call__(self, *args, **kwargs):
        """Run the executable with subprocess.check_output, return output."""
        return_output = kwargs.get("return_output", False)
        fail_on_error = kwargs.get("fail_on_error", True)

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn("Quotes in command arguments can confuse scripts like configure.",
                     "The following arguments may cause problems when executed:",
                     str("\n".join(["    "+arg for arg in quoted_args])),
                     "Quotes aren't needed because spack doesn't use a shell.",
                     "Consider removing them")

        cmd = self.exe + list(args)
        tty.verbose(" ".join(cmd))

        try:
            proc = subprocess.Popen(
                cmd,
                stderr=sys.stderr,
                stdout=subprocess.PIPE if return_output else sys.stdout)
            out, err = proc.communicate()
            self.returncode = proc.returncode

            if fail_on_error and proc.returncode != 0:
                raise SpackError("command '%s' returned error code %d"
                                 % (" ".join(cmd), proc.returncode))
            if return_output:
                return out

        except subprocess.CalledProcessError, e:
            if fail_on_error: raise

    def __repr__(self):
        return "<exe: %s>" % self.exe


def which(name, **kwargs):
    """Finds an executable in the path like command-line which."""
    path     = kwargs.get('path', os.environ.get('PATH', '').split(os.pathsep))
    required = kwargs.get('required', False)

    if not path:
        path = []

    for dir in path:
        exe = os.path.join(dir, name)
        if os.access(exe, os.X_OK):
            return Executable(exe)

    if required:
        tty.die("spack requires %s.  Make sure it is in your path." % name)
    return None
