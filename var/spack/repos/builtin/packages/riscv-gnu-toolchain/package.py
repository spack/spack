# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import shlex
from subprocess import PIPE, Popen

from spack import *
from spack.repo import GitExe

class RiscvGnuToolchain(Package):
    """A cross-compilation tool for RISC-V.
    """

    homepage = "https://spack-tutorial.readthedocs.io/"
    git = "https://github.com/riscv-collab/riscv-gnu-toolchain.git"
    
    phases = ['configure', 'build']
    build_targets = ""
    if "+Newlib" in self.spec:
        build_targets = ""
    elif "+Linux" in self.spec:
        build_targets = "linux"

    maintainers = ['wanlinwang']

    version('develop', branch='master', submodules=True)
    version('2022.08.08', tag='2022.08.08', submodules=True)

    # Dependencies:
    depends_on('autoconf', type=('build', 'link'))
    depends_on('automake', type=('build', 'link'))
    depends_on('python', type=('build', 'link'))
    depends_on('gawk', type=('build', 'link'))
    depends_on('bison', type=('build', 'link'))
    depends_on('flex@:2.6.1,2.6.4:', type=('build', 'link'))
    depends_on('texinfo', type=('build', 'link'))
    depends_on('patchutils', type=('build', 'link'))
    depends_on('mpc', type=('build', 'link'))
    depends_on('gmp', type=('build', 'link'))
    depends_on('mpfr', type=('build', 'link'))
    depends_on('gcc', type=('build', 'link'))
    depends_on('zlib', type=('build', 'link'))
    depends_on('expat', type=('build', 'link'))

    variant("Newlib", default=True, description="To build the Newlib cross-compiler.")
    variant("Linux", default=False, description="To build the Linux cross-compiler.")


    def configure_args(self):
        spec   = self.spec
        prefix = self.prefix

        config_args = [] 
        return config_args


    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """

        with working_dir(self.stage.source_path, create=True):
            options = getattr(self, 'configure_flag_args', [])
            options += ['--prefix={0}'.format(prefix)]
            options += self.configure_args()
            configure(*options)


    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """

        # configure and build in one step
        with working_dir(self.stage.source_path):
            # modify Makefile not to git init submodules.
            # /bin/sed -i -r '/^# Rule for auto init submodules/,/git submodule update.*$/d' Makefile
            cmd = "/bin/sed -i -r '/^# Rule for auto init submodules/,/git submodule update.*$/d' Makefile"
            p = Popen(shlex.split(cmd))
            p.communicate()

            params = self.build_targets
            make(*params)
