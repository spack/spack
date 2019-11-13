# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Z3(MakefilePackage):
    """Z3 is a theorem prover from Microsoft Research.
    It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3/wiki"
    url      = "https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz"

    version('4.5.0', sha256='aeae1d239c5e06ac183be7dd853775b84698db1265cb2258e5918a28372d4a0c')
    version('4.4.1', sha256='50967cca12c5c6e1612d0ccf8b6ebf5f99840a783d6cf5216336a2b59c37c0ce')
    version('4.4.0', sha256='65b72f9eb0af50949e504b47080fb3fc95f11c435633041d9a534473f3142cba')

    phases = ['bootstrap', 'build', 'install']

    variant('python', default=False, description='Enable python support')
    depends_on('python', when='+python')

    build_directory = 'build'

    def configure_args(self):
        spec = self.spec
        return [
            '--python' if '+python' in spec else ''
        ]

    def bootstrap(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()
        spec['python'].command('scripts/mk_make.py', *options)
