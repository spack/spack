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

from llnl.util.filesystem import *
import llnl.util.tty as tty

import spack
import spack.modules

# Character limit for shebang line.  Using Linux's 127 characters
# here, as it is the shortest I could find on a modern OS.
shebang_limit = 127

def shebang_too_long(path):
    """Detects whether a file has a shebang line that is too long."""
    with open(path, 'r') as script:
        bytes = script.read(2)
        if bytes != '#!':
            return False

        line = bytes + script.readline()
        return len(line) > shebang_limit


def filter_shebang(path):
    """Adds a second shebang line, using sbang, at the beginning of a file."""
    with open(path, 'r') as original_file:
        original = original_file.read()

    # This line will be prepended to file
    new_sbang_line = '#!/bin/bash %s/bin/sbang\n' % spack.spack_root

    # Skip files that are already using sbang.
    if original.startswith(new_sbang_line):
        return

    backup = path + ".shebang.bak"
    os.rename(path, backup)

    with open(path, 'w') as new_file:
        new_file.write(new_sbang_line)
        new_file.write(original)

    copy_mode(backup, path)
    unset_executable_mode(backup)

    tty.warn("Patched overly long shebang in %s" % path)


def filter_shebangs_in_directory(directory):
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        # only handle files
        if not os.path.isfile(path):
            continue

        # only handle links that resolve within THIS package's prefix.
        if os.path.islink(path):
            real_path = os.path.realpath(path)
            if not real_path.startswith(directory + os.sep):
                continue

        # test the file for a long shebang, and filter
        if shebang_too_long(path):
            filter_shebang(path)


def post_install(pkg):
    """This hook edits scripts so that they call /bin/bash
       $spack_prefix/bin/sbang instead of something longer than the
       shebang limit."""
    if not os.path.isdir(pkg.prefix.bin):
        return
    filter_shebangs_in_directory(pkg.prefix.bin)
