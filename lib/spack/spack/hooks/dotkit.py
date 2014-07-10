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
import re
import textwrap
import shutil
from contextlib import closing

from llnl.util.filesystem import join_path, mkdirp

import spack


class DotkitFile(object):
    def __init__(self, path):
        self.dk_file = open(path, 'w')

    def close(self):
        self.dk_file.close()

    def write(self, *args):
        self.dk_file.write(*args)

    def alter(self, var, path):
        self.dk_file.write("dk_alter %s %s\n" % (var, path))

    def setenv(self, var, value):
        self.dk_file.write("dk_setenv %s %s\n" % (var, value))


def dotkit_file(pkg):
    dk_file_name = pkg.spec.format('$_$@$%@$+$=$#') + ".dk"
    return join_path(spack.dotkit_path, dk_file_name)


def post_install(pkg):
    if not os.path.exists(spack.dotkit_path):
        mkdirp(spack.dotkit_path)

    alterations = []
    for var, path in [
        ('PATH', pkg.prefix.bin),
        ('MANPATH', pkg.prefix.man),
        ('MANPATH', pkg.prefix.share_man),
        ('LD_LIBRARY_PATH', pkg.prefix.lib),
        ('LD_LIBRARY_PATH', pkg.prefix.lib64)]:

        if os.path.isdir(path):
            alterations.append((var, path))

    if not alterations:
        return

    alterations.append(("CMAKE_PREFIX_PATH", pkg.prefix))

    dk_file = dotkit_file(pkg)
    with closing(DotkitFile(dk_file)) as dk:
        # Put everything in the spack category.
        dk.write('#c spack\n')

        dk.write('#d %s\n' % pkg.spec.format("$_ $@"))

        # Recycle the description
        if pkg.__doc__:
            doc = re.sub(r'\s+', ' ', pkg.__doc__)
            for line in textwrap.wrap(doc, 72):
                dk.write("#h %s\n" % line)

        # Write alterations
        for alt in alterations:
            dk.alter(*alt)

        # callback in case package has extensions.
        dotkit_fun = getattr(pkg, 'dotkit', None)
        if dotkit_fun and hasattr(dotkit_fun, '__call__'):
            dotkit_fun(dk)


def post_uninstall(pkg):
    dk_file = dotkit_file(pkg)
    if os.path.exists(dk_file):
        shutil.rmtree(dk_file, ignore_errors=True)

