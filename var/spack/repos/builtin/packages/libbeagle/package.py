# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbeagle(AutotoolsPackage):
    """Beagle performs genotype calling, genotype phasing, imputation of
       ungenotyped markers, and identity-by-descent segment detection."""

    homepage = "https://github.com/beagle-dev/beagle-lib"
    url      = "https://github.com/beagle-dev/beagle-lib/archive/beagle_release_2_1_2.tar.gz"

    version('2.1.2', '1107614e86f652f8ee45c1c92f2af3d4')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('subversion', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('java', type='build')

    def url_for_version(self, version):
        url = "https://github.com/beagle-dev/beagle-lib/archive/beagle_release_{0}.tar.gz"
        return url.format(version.underscored)

    def setup_environment(self, spack_env, run_env):
        prefix = self.prefix
        run_env.prepend_path('BEAST_LIB', prefix.lib)
