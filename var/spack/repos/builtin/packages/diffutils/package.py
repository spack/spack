# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Diffutils(AutotoolsPackage, GNUMirrorPackage):
    """GNU Diffutils is a package of several programs related to finding
    differences between files."""

    tags = ['core-packages']

    executables = [r'^diff$']

    homepage = "https://www.gnu.org/software/diffutils/"
    gnu_mirror_path = "diffutils/diffutils-3.7.tar.xz"

    version('3.8', sha256='a6bdd7d1b31266d11c4f4de6c1b748d4607ab0231af5188fc2533d0ae2438fec')
    version('3.7', sha256='b3a7a6221c3dc916085f0d205abf6b8e1ba443d4dd965118da364a1dc1cb3a26')
    version('3.6', sha256='d621e8bdd4b573918c8145f7ae61817d1be9deb4c8d2328a65cea8e11d783bd6')

    build_directory = 'spack-build'

    patch('nvhpc.patch', when='@3.7 %nvhpc')
    patch('intprops-workaround-nvc-22.1-bug.patch', sha256='146b7021bb0a304a3d1c0638956c4e735c2076d292d238f2806efadc972d99e5', when='@3.8 %nvhpc')

    conflicts('%nvhpc', when='@:3.6,3.8:')
    # See configure_args() for details on %intel@19 compilers
    conflicts('%intel@19.0.0:19')

    depends_on('iconv')

    def setup_build_environment(self, env):
        if self.spec.satisfies('%fj'):
            env.append_flags('CFLAGS',
                             '-Qunused-arguments')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'diff \(GNU diffutils\) (\S+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        args = []
        # See issue #31418.
        if self.spec.satisfies('%intel@14:15'):
            args.append('CFLAGS=-no-gcc')
        # For %intel@19 comment out the conflict() above and uncomment
        # the next two lines.  Modify the path to point to a recent version
        # of gcc on your machine.  gcc@4.9.3 is known not to work.
        # if self.spec.satisfies('%intel@19'):
        #    args.append('CFLAGS=-gcc-name=/usr/tce/packages/gcc/gcc-10.2.1/bin/gcc')
        return args
