# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Coreutils(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Core Utilities are the basic file, shell and text
       manipulation utilities of the GNU operating system.  These are
       the core utilities which are expected to exist on every
       operating system.
    """

    homepage = 'https://www.gnu.org/software/coreutils/'
    gnu_mirror_path = 'coreutils/coreutils-8.26.tar.xz'

    tags = ['core-packages']

    version('9.1', sha256='61a1f410d78ba7e7f37a5a4f50e6d1320aca33375484a3255eddf17a38580423')
    version('9.0', sha256='ce30acdf4a41bc5bb30dd955e9eaa75fa216b4e3deb08889ed32433c7b3b97ce')
    version('8.32', sha256='4458d8de7849df44ccab15e16b1548b285224dbba5f08fac070c1c0e0bcc4cfa')
    version('8.31', sha256='ff7a9c918edce6b4f4b2725e3f9b37b0c4d193531cac49a48b56c4d0d3a9e9fd')
    version('8.30', sha256='e831b3a86091496cdba720411f9748de81507798f6130adeaef872d206e1b057')
    version('8.29', sha256='92d0fa1c311cacefa89853bdb53c62f4110cdfda3820346b59cbd098f40f955e')
    version('8.26', sha256='155e94d748f8e2bc327c66e0cbebdb8d6ab265d2f37c3c928f7bf6c3beba9a8e')
    version('8.23', sha256='ec43ca5bcfc62242accb46b7f121f6b684ee21ecd7d075059bf650ff9e37b82d')

    variant("gprefix", default=False, description="prefix commands with 'g', to avoid conflicts with OS utilities")

    patch('https://src.fedoraproject.org/rpms/coreutils/raw/6b50cb9f/f/coreutils-8.32-ls-removed-dir.patch',
          when='@8.32 target=aarch64:',
          sha256='5878894375a8fda98150783430b30c0b7104899dc5522034ebcaf8c961183b7e')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        configure_args = []
        if spec.satisfies('platform=darwin'):
            if "+gprefix" in self.spec:
                configure_args.append('--program-prefix=g')
            configure_args.append('--without-gmp')
            configure_args.append('gl_cv_func_ftello_works=yes')

        return configure_args
