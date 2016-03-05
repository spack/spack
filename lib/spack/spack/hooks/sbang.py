##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

from llnl.util.filesystem import *
import llnl.util.tty as tty

import spack
import spack.modules

# Character limit for shebang line.  Using Linux's 127 characters
# here, as it is the shortest I could find on a modern OS.
shebang_limit = 127

def shebang_too_long(path):
    """Detects whether an file has a shebang line that is too long."""
    with open(path, 'r') as script:
        bytes = script.read(2)
        if bytes != '#!':
            return False

        line = bytes + script.readline()
        return len(line) > shebang_limit


def filter_shebang(path):
    """Adds a second shebang line, using sbang, at the beginning of a file."""
    backup = path + ".shebang.bak"
    os.rename(path, backup)

    with open(backup, 'r') as bak_file:
        original = bak_file.read()

    with open(path, 'w') as new_file:
        new_file.write('#!/bin/bash %s/bin/sbang\n' % spack.spack_root)
        new_file.write(original)

    copy_mode(backup, path)
    unset_executable_mode(backup)

    tty.warn("Patched overly long shebang in %s" % path)


def post_install(pkg):
    """This hook edits scripts so that they call /bin/bash
       $spack_prefix/bin/sbang instead of something longer than the
       shebang limit."""
    if not os.path.isdir(pkg.prefix.bin):
        return

    for file in os.listdir(pkg.prefix.bin):
        path = os.path.join(pkg.prefix.bin, file)
        if shebang_too_long(path):
            filter_shebang(path)

