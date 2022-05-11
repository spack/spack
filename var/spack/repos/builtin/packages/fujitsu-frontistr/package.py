# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *
from spack.pkg.builtin.frontistr import FrontistrBase


class FujitsuFrontistr(FrontistrBase):
    """This is a fork repository of the FrontISTR tuned for A64FX."""

    _name = 'fujitsu-frontistr'
    homepage = "https://www.frontistr.com/"
    url = "https://github.com/fujitsu/FrontISTR/archive/refs/tags/v5.2_tuned.tar.gz"
    git      = "https://github.com/fujitsu/FrontISTR"
    maintainers = ['kinagaki-fj', 'kinagaki', 'm-shunji']

    version('master', branch='fj-master')
    version('5.2', sha256='ebf73a96c33ae7c9e616c99f9ce07ec90d802764dbf6abf627b0083c3bbd2b2e')
    version('5.0', sha256='7a3a2dd0f834048fb71cc254c9da6c2637fb23110e79b5efaf208d6f69a5b30a')

    variant('static', default=True, description='Build with static linkage')
    depends_on('metis ~shared', when='+static')
    depends_on('mumps ~shared', when='+static')
    depends_on('trilinos ~shared', when='+static')

    def url_for_version(self, version):
        url = "https://github.com/fujitsu/FrontISTR/archive/refs/tags/v{0}_tuned.tar.gz"
        return url.format(version)

    def cmake_args(self):
        define = CMakePackage.define
        args = super(FujitsuFrontistr, self).cmake_args()
        if self.spec.satisfies('%fj'):
            args.extend([
                define('CMAKE_C_FLAGS',
                       '-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2'),
                define('CMAKE_CXX_FLAGS',
                       '-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2'),
                define('CMAKE_Fortran_FLAGS',
                       '-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2'),
                define('CMAKE_Fortran_MODDIR_FLAG', 'M'),
                define('OpenMP_C_FLAGS', '-Kopenmp'),
                define('OpenMP_CXX_FLAGS', '-Kopenmp'),
                define('OpenMP_Fortran_FLAGS', '-Kopenmp')
            ])
        return args
