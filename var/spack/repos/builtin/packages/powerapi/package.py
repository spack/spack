# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Powerapi(AutotoolsPackage):
    """This software is a reference implementation of the PowerAPI"""

    homepage = "https://powerapi.sandia.gov/"
    git      = "https://github.com/pwrapi/pwrapi-ref.git"

    version('1.1.1', commit='93f66dfa29f014067823f2b790a1862e5841a11c')

    variant('hwloc', default=False, description='Build hwloc support')
    variant('debug', default=False, description='Enable debug support')
    variant('mpi',   default=False, description='Enable MPI support')
    variant('package', default=False, description='Enable package support')
    variant('gnu-ld', default=False, description='Assume GNU compiled uses gnu-ld')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('m4')

    depends_on('hwloc', when='+hwloc')
    depends_on('mpi', when='+mpi')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        self = self.spec
        args = []

        if '+hwloc' in self.spec:
            args.append('--with-hwloc={0}'.format(self['hwloc'].prefix))

        if '+mpi' in self.spec:
            args.append('--with-mpi={0}'.format(self['mpi'].prefix))

        args.extend([
            '--with-PACKAGE=%' % ('yes' if '+package' in spec else 'no'),
            '--with%-gnu-ld' % ('' if '+gnu-ld' in spec else 'out'),
            '--%able-debug' % ('en' if '+debug' in spec else 'dis')
        ])

        return args

    def install(self, spec, prefix):
        make('install')
