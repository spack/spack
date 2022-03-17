# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scsumma25d(MakefilePackage):
    """A new parallel matrix multiplication routine using the 2.5D algorithm """

    homepage = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/25dpdgemm"
    url      = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/25dpdgemm/scsumma25d-1.0a.tgz"

    version('1.0a', sha256='c6dc0a758e3f9e633c25edcf8385415a8be83e1ccdd5b73a425d11fa1969f61d')

    depends_on('mpi')
    depends_on('scalapack')

    @property
    def build_targets(self):
        targets = []

        cppflags = ''
        if '^intel-mkl' in self.spec:
            cppflags = '-DICC'

        targets.append('CXX={0}'.format(self.spec['mpi'].mpicxx))
        targets.append('FLAGS={0} {1} {2} {3}'
                       .format(self.compiler.openmp_flag,
                               self.spec['scalapack'].libs.link_flags,
                               self.spec['blas'].libs.link_flags,
                               cppflags))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        install(join_path('lib', 'libscsumma25d.a'),  prefix.lib)
        install(join_path('include', 'scsumma25d.h'), prefix.include)
