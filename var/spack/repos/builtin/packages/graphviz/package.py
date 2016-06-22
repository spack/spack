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


class Graphviz(Package):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae', url="http://pkgs.fedoraproject.org/repo/pkgs/graphviz/graphviz-2.38.0.tar.gz/5b6a829b2ac94efcd5fa3c223ed6d3ae/graphviz-2.38.0.tar.gz")

    # We try to leave language bindings enabled if they don't cause build issues
    # or add dependencies.
    variant('swig', default=False,
        description='Enable for optional swig language bindings.')
    variant('sharp', default=True,
        description='Enable for optional sharp language bindings.')
    variant('go', default=False,
        description='Enable for optional go language bindings.')
    variant('guile', default=True,
        description='Enable for optional guile language bindings.')
    variant('io', default=False,
        description='Enable for optional io language bindings.')
    variant('java', default=False,  # Spack has no Java support
        description='Enable for optional java language bindings.')
    variant('lua', default=True,
        description='Enable for optional lua language bindings.')
    variant('ocaml', default=True,
        description='Enable for optional ocaml language bindings.')
    variant('perl', default=False,    # Spack has no Perl support
        description='Enable for optional perl language bindings.')
    variant('php', default=True,
        description='Enable for optional php language bindings.')
    variant('python', default=False,    # Build issues with Python 2/3
        description='Enable for optional python language bindings.')
    variant('r', default=True,
        description='Enable for optional r language bindings.')
    variant('ruby', default=True,
        description='Enable for optional ruby language bindings.')
    variant('tcl', default=True,
        description='Enable for optional tcl language bindings.')

    parallel = False

    depends_on("swig", when='+swig')
    # Graphviz does not work with Python3
    depends_on("python@2:2.8", when='+python')
    depends_on("ghostscript")
    depends_on("pkg-config")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]


        vars = ('+swig', '+sharp', '+go', '+guile', '+io',
            '+java', '+lua', '+ocaml', '+perl', '+php',
            '+python', '+r', '+ruby', '+tcl')

        for var in vars:
            enable = 'enable' if (var in spec) else 'disable'
            options.append('--%s-%s' % (enable, var[1:]))

        # On OSX fix the compiler error:
        # In file included from tkStubLib.c:15:
        # /usr/include/tk.h:78:11: fatal error: 'X11/Xlib.h' file not found
        #       include <X11/Xlib.h>
        if sys.platform == 'darwin':
            options.append('CFLAGS=-I/opt/X11/include')

        configure(*options)
        make()
        make("install")
