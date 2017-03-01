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
    homepage = 'http://www.graphviz.org'
    url      = 'http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz'

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    # We try to leave language bindings enabled if they don't cause
    # build issues or add dependencies.
    variant('swig', default=False,
            description='Enable for optional swig language bindings'
            ' (not yet functional)')
    variant('sharp', default=False,
            description='Enable for optional sharp language bindings'
            ' (not yet functional)')
    variant('go', default=False,
            description='Enable for optional go language bindings'
            ' (not yet functional)')
    variant('guile', default=False,
            description='Enable for optional guile language bindings'
            ' (not yet functional)')
    variant('io', default=False,
            description='Enable for optional io language bindings'
            ' (not yet functional)')
    variant('java', default=False,  # Spack has no Java support
            description='Enable for optional java language bindings')
    variant('lua', default=False,
            description='Enable for optional lua language bindings'
            ' (not yet functional)')
    variant('ocaml', default=False,
            description='Enable for optional ocaml language bindings'
            ' (not yet functional)')
    variant('perl', default=False,    # Spack has no Perl support
            description='Enable for optional perl language bindings')
    variant('php', default=False,
            description='Enable for optional php language bindings'
            ' (not yet functional)')
    variant('python', default=False,    # Build issues with Python 2/3
            description='Enable for optional python language bindings'
            ' (not yet functional)')
    variant('r', default=False,
            description='Enable for optional r language bindings'
            ' (not yet functional)')
    variant('ruby', default=False,
            description='Enable for optional ruby language bindings'
            ' (not yet functional)')
    variant('tcl', default=False,
            description='Enable for optional tcl language bindings'
            ' (not yet functional)')

    parallel = False

    depends_on('swig', when='+swig')
    depends_on('ghostscript')
    depends_on('freetype')
    depends_on('expat')
    depends_on('libtool')
    depends_on('pkg-config', type='build')

    depends_on('jdk', when='+java')
    depends_on('python@2:2.8', when='+python')

    def configure_args(self):
        spec = self.spec
        options = []

        # These language bindings have been tested, we know they work.
        tested_bindings = ('+java', '+perl')

        # These language bindings have not yet been tested.  They
        # likely need additional dependencies to get working.
        untested_bindings = (
            '+swig', '+sharp', '+go', '+guile', '+io',
            '+lua', '+ocaml', '+php',
            '+python', '+r', '+ruby', '+tcl')

        for var in untested_bindings:
            if var in spec:
                raise SpackException(
                    "The variant {0} for language bindings has not been "
                    "tested.  It might or might not work.  To try it "
                    "out, run `spack edit graphviz`, and then move '{0}' "
                    "from the `untested_bindings` list to the "
                    "`tested_bindings` list.  Be prepared to add "
                    "required dependencies.  "
                    "Please then submit a pull request to "
                    "http://github.com/llnl/spack")

        for var in tested_bindings:
            enable = 'enable' if (var in spec) else 'disable'
            options.append('--%s-%s' % (enable, var[1:]))

        # On OSX fix the compiler error:
        # In file included from tkStubLib.c:15:
        # /usr/include/tk.h:78:11: fatal error: 'X11/Xlib.h' file not found
        #       include <X11/Xlib.h>
        if sys.platform == 'darwin':
            options.append('CFLAGS=-I/opt/X11/include')

        # A hack to patch config.guess in the libltdl sub directory
        shutil.copyfile('./config/config.guess', 'libltdl/config/config.guess')

        return options
