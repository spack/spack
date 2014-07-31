##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
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


def module_file(pkg):
    m_file_name = pkg.spec.format('$_$@$%@$+$=$#')
    return join_path(spack.module_path, m_file_name)


def post_install(pkg):
    if not os.path.exists(spack.module_path):
        mkdirp(spack.module_path)

    alterations = []
    for var, path in [
        ('PATH', pkg.prefix.bin),
        ('MANPATH', pkg.prefix.man),
        ('MANPATH', pkg.prefix.share_man),
        ('LD_LIBRARY_PATH', pkg.prefix.lib),
        ('LD_LIBRARY_PATH', pkg.prefix.lib64)]:

        if os.path.isdir(path):
            alterations.append("prepend_path %s %s\n" % (var, path))

    if not alterations:
        return

    alterations.append("prepend_path CMAKE_PREFIX_PATH %s\n" % pkg.prefix)

    m_file = module_file(pkg)
    with closing(open(m_file, 'w')) as m:
        # Put everything in the spack category.
        m.write('#%Module1.0\n')

        m.write('module-whatis \"%s\"\n' % pkg.spec.format("$_ $@"))

        # Recycle the description
        if pkg.__doc__:
            m.write('proc ModulesHelp { } {\n')
            doc = re.sub(r'\s+', ' ', pkg.__doc__)
            m.write("puts str \"%s\"\n" % doc)
            m.write('}')


        # Write alterations
        for alter in alterations:
            m.write(alter)


def post_uninstall(pkg):
    m_file = module_file(pkg)
    if os.path.exists(m_file):
        shutil.rmtree(m_file, ignore_errors=True)

