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

    version('4.5.0', 'f332befa0d66d81818a06279a0973e25')
    version('4.4.1', '4336a9df24f090e711c6d42fd4e2b1fc')
    version('4.4.0', '2bcbb0381cc1572cace99aac8af08990')

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
