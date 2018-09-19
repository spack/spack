##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Openbabel(CMakePackage):
    """Open Babel is a chemical toolbox designed to speak the many languages
    of chemical data. It's an open, collaborative project allowing anyone to
    search, convert, analyze, or store data from molecular modeling, chemistry,
    solid-state materials, biochemistry, or related areas."""

    homepage = "http://openbabel.org/wiki/Main_Page"
    url      = "https://sourceforge.net/projects/openbabel/files/openbabel/2.4.1/openbabel-2.4.1.tar.gz"

    version('2.4.1', 'd9defcd7830b0592fece4fe54a137b99')

    variant('python', default=True, description='Build Python bindings')

    extends('python', when='+python')

    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('cmake@2.4.8:', type='build')
    depends_on('pkgconfig',   type='build')
    depends_on('cairo')       # required to support PNG depiction
    depends_on('eigen@3.0:')  # required if using the language bindings
    depends_on('libxml2')     # required to read/write CML files, XML formats
    depends_on('zlib')        # required to support reading gzipped files

    # Needed for Python 3.6 support
    patch('python-3.6-rtld-global.patch', when='@:2.4.1+python')

    # Convert tabs to spaces. Allows unit tests to pass
    patch('testpdbformat-tabs-to-spaces.patch', when='@:2.4.1')

    def cmake_args(self):
        spec = self.spec
        args = []

        if '+python' in spec:
            args.extend([
                '-DPYTHON_BINDINGS=ON',
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
            ])
        else:
            args.append('-DPYTHON_BINDINGS=OFF')

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        obabel = Executable(join_path(self.prefix.bin, 'obabel'))
        obabel('-:C1=CC=CC=C1Br', '-omol')

        if '+python' in self.spec:
            # Attempt to import the Python modules
            for module in ['openbabel', 'pybel']:
                python('-c', 'import {0}'.format(module))
