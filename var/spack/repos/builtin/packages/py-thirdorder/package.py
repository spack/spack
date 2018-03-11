##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-thirdorder
#
# You can edit this file again by typing:
#
#     spack edit py-thirdorder
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *

class PyThirdorder(PythonPackage):
    """Thirdorder scripts helps users of ShengBTE and almaBTE FORCE\_CONSTANTS\_3RD files in an efficient and convenient manner"""

    homepage = "http://www.shengbte.org"
    url      = "http://www.shengbte.org/downloads/thirdorder-v1.1.1-8526f47.tar.bz2"

    version('1.1.1-8526f47', 'c39ff34056a0e57884a6ff262581dbbe')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-scipy',        type=('build', 'run'))
    depends_on('spglib',        type=('build', 'run'))

    def patch(self):
      makefile = FileFilter('setup.py')
      makefile.filter('LIBRARY_DIRS = .*', 'LIBRARY_DIRS = ["%s"]' % self.spec['spglib'].prefix.lib)
      makefile.filter('INCLUDE_DIRS = .*', 'INCLUDE_DIRS = ["%s"]' % self.spec['spglib'].prefix.include)

      makefile = FileFilter('thirdorder_core.c')
      makefile.filter('#include "spglib.*"', '#include "spglib.h"')

    def post_install(self, spec, prefix):
      mkdirp(prefix.bin)
      install('thirdorder_espresso.py', prefix.bin+'thirdorder_espresso.py')
      install('thirdorder_vasp.py', prefix.bin+'thirdorder_vasp.py')
      install('thirdorder_castep.py', prefix.bin+'thirdorder_castep.py')

    def test(self):
      pass
