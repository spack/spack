# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vampirtrace(AutotoolsPackage):
    """VampirTrace is an open source library that allows detailed logging of
    program execution for parallel applications using message passing (MPI)
    and threads (OpenMP, Pthreads)."""

    homepage = "https://tu-dresden.de/zih/forschung/projekte/vampirtrace"
    url      = "http://wwwpub.zih.tu-dresden.de/~mlieber/dcount/dcount.php?package=vampirtrace&get=VampirTrace-5.14.4.tar.gz"

    version('5.14.4', '1c92b23169df9bcc860e5fc737dbc9c9')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('mpi', when='+mpi')
    depends_on('otf')
    depends_on('papi')
    depends_on('zlib')

    def patch(self):
        path = 'tools/vtwrapper/vt{0}-wrapper-data.txt.in'

        for wrapper in ('cc', 'c++', 'fort'):
            filter_file('@VT_WRAPPER_OPARI_TAB_COMPILER@',
                        '@VT_WRAPPER_CC_COMPILER@',
                        path.format(wrapper))

    def configure_args(self):
        spec = self.spec
        compiler = self.compiler

        args = [
            '--with-extern-otf',
            '--with-extern-otf-dir={0}'.format(spec['otf'].prefix),
            '--with-papi-dir={0}'.format(spec['papi'].prefix),
            '--with-zlib-dir={0}'.format(spec['zlib'].prefix),
            '--with-wrapper-cc-compiler={0}'.format(compiler.cc),
            '--with-wrapper-cc-cpp={0} -E'.format(compiler.cc),
            '--with-wrapper-cxx-compiler={0}'.format(compiler.cxx),
            '--with-wrapper-cxx-cpp={0} -E'.format(compiler.cxx),
            '--with-wrapper-fc-compiler={0}'.format(compiler.fc),
            '--with-wrapper-fc-cpp={0} -E'.format(compiler.fc)
        ]

        if '+mpi' in spec:
            args.append('--with-mpi-dir={0}'.format(spec['mpi'].prefix))

        return args
