# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ntl(Package):
    """
    NTL  -- a library for doing number theory

    NTL is open-source software distributed under the terms of the GNU Lesser
    General Public License (LGPL) version 2.1 or later.  See the file
    doc/copying.txt for complete details on the licensing of NTL.

    Documentation is available in the file doc/tour.html, which can be viewed
    with a web browser.

    """

    homepage = "https://libntl.org"
    url      = "https://github.com/libntl/ntl/archive/refs/tags/v11.5.1.tar.gz"

    maintainers = ['wohlbier']

    version('11.5.1', sha256='ef578fa8b6c0c64edd1183c4c303b534468b58dd3eb8df8c9a5633f984888de5')
    version('11.5.0', sha256='9e1e6488b177c3e5d772fdd6279c890937a9d1c3b694a904ac1cfbe9cab836db')
    version('11.4.4', sha256='2ce7a10fadbed6c3859d72c859612a4ca0dbdf6a9db99db4261422b7f0804bfa')

    variant('shared', default=False, description='Build shared library.')

    depends_on('gmp')

    phases = ['configure', 'build', 'install']

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        config_args = [
            'CXX={0}'.format(self.compiler.cxx),
            'DEF_PREFIX={0}'.format(prefix),
            'GMP_PREFIX={0}'.format(spec['gmp'].prefix)  # gmp dependency
        ]
        if '+shared' in spec:
            config_args.append('SHARED=on')

        return config_args

    def configure(self, spec, prefix):
        with working_dir('src'):
            configure = Executable('./configure')
            configure(*self.configure_args())

    def build(self, spec, prefix):
        with working_dir('src'):
            make()

    def install(self, spec, prefix):
        with working_dir('src'):
            make('install')
