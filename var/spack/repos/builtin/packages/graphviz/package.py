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
from spack import *
import sys
import shutil


class Graphviz(AutotoolsPackage):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    # By default disable optional Perl language support to prevent build issues
    # related to missing Perl packages. If spack begins support for Perl in the
    # future, this package can be updated to depend_on('perl') and the
    # ncecessary devel packages.
    variant(
        'perl', default=False,
        description='Enable if you need the optional Perl language bindings.')

    parallel = False

    depends_on("swig")
    depends_on("python")
    depends_on("ghostscript")
    depends_on("freetype")
    depends_on("libtool", type='build')
    depends_on("pkg-config", type='build')

    def configure_args(self):
        options = []
        if '+perl' not in self.spec:
            options.append('--disable-perl')

        # On OSX fix the compiler error:
        # In file included from tkStubLib.c:15:
        # /usr/include/tk.h:78:11: fatal error: 'X11/Xlib.h' file not found
        #       include <X11/Xlib.h>
        if sys.platform == 'darwin':
            options.append('CFLAGS=-I/opt/X11/include')
        options.append('--with-ltdl-lib=%s/lib' % self.spec['libtool'].prefix)

        # A hack to patch config.guess in the libltdl sub directory
        shutil.copyfile('./config/config.guess', 'libltdl/config/config.guess')

        return options
