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
from subprocess import call
from os import chdir
import platform

class PyThirdorder(Package):
    """Thirdorder scripts helps users of ShengBTE and almaBTE FORCE\_CONSTANTS\_3RD files in an efficient and convenient manner"""

    homepage = "http://www.shengbte.org"
    url      = "http://www.shengbte.org/downloads/thirdorder-v1.1.1-8526f47.tar.bz2"

    version('1.1.1-8526f47', 'c39ff34056a0e57884a6ff262581dbbe')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-scipy',        type=('build', 'run'))
    depends_on('spglib',        type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):    
      python_version = self.spec['python'].version.up_to(2)
      arch = '{0}-{1}'.format(platform.system().lower(), platform.machine())
        
      run_env.prepend_path('PYTHONPATH', join_path(self.spec['python'].prefix.lib, 'python{0}'.format(python_version), 'site-packages'))
      run_env.prepend_path('LIBRARY_PATH', self.spec ['python'].prefix.lib)
      run_env.prepend_path('LD_LIBRARY_PATH', self.spec['python'].prefix.lib)

      run_env.prepend_path('PYTHONPATH', join_path(prefix.lib, 'python{0}'.format(python_version), 'site-packages'))
      run_env.prepend_path('LIBRARY_PATH', prefix.lib)
      run_env.prepend_path('LD_LIBRARY_PATH', prefix.lib)

      run_env.prepend_path('PYTHONPATH', join_path(self.spec['py-numpy'].prefix.lib, 'python{0}'.format(python_version), 'site-packages'))
      run_env.prepend_path('LIBRARY_PATH', self.spec ['py-numpy'].prefix.lib)
      run_env.prepend_path('LD_LIBRARY_PATH', self.spec['py-numpy'].prefix.lib)

      run_env.prepend_path('PYTHONPATH', join_path(self.spec['py-scipy'].prefix.lib, 'python{0}'.format(python_version), 'site-packages'))
      run_env.prepend_path('LIBRARY_PATH', self.spec['py-scipy'].prefix.lib)
      run_env.prepend_path('LD_LIBRARY_PATH', self.spec['py-scipy'].prefix.lib)

    def patch(self):
      makefile = FileFilter('setup.py')
      makefile.filter('LIBRARY_DIRS = .*', 'LIBRARY_DIRS = ["%s"]' % self.spec['spglib'].prefix.lib)
      makefile.filter('INCLUDE_DIRS = .*', 'INCLUDE_DIRS = ["%s"]' % self.spec['spglib'].prefix.include)

      makefile = FileFilter('thirdorder_core.c')
      makefile.filter('#include "spglib.*"', '#include "spglib.h"')

    # @run_after('install')
    # @on_package_attributes(run_tests=True)
    def install(self, spec, prefix):
      call(['python', 'setup.py', 'build'])
      call(['python', 'setup.py', 'install', '--prefix=%s' % prefix])
      mkdirp(prefix.bin)
      install('thirdorder_espresso.py', prefix.bin)
      install('thirdorder_vasp.py', prefix.bin)
      install('thirdorder_castep.py', prefix.bin)
      install('thirdorder_common.py', prefix.bin)
      #print 'Run tests? %s' % self.run_tests
      if self.run_tests:
        self.check_install()

    def check_install(self):
      python('-c', 'import thirdorder_core')
      with open('POSCAR','w') as testfile:
        testfile.writelines('InAs\n   6.00000000000000\n     0.0000000000000000    0.5026468896190005    0.5026468896190005\n     0.5026468896190005    0.0000000000000000    0.5026468896190005\n     0.5026468896190005    0.5026468896190005    0.0000000000000000\n   In   As\n   1   1\nDirect\n  0.0000000000000000  0.0000000000000000  0.0000000000000000\n  0.2500000000000000  0.2500000000000000  0.2500000000000000')
      #with working_dir('..'):
      call(['%s/thirdorder_vasp.py' % prefix.bin, 'sow', '4', '4', '4', '-3'])
