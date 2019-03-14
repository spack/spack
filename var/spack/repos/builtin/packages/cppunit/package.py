# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cppunit(AutotoolsPackage):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url = "http://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"

    version('1.13.2', '0eaf8bb1dcf4d16b12bec30d0732370390d35e6f')

    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def setup_environment(self, spack_env, run_env):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = '' if cxxstd == 'default' else \
                     getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        spack_env.append_flags('CXXFLAGS', cxxstdflag)
