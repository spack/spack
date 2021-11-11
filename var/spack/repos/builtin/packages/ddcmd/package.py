# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *
import llnl.util.tty as tty


class Ddcmd(CMakePackage, CudaPackage):

    homepage = "https://github.com/LLNL/ddcMD"
    git      = "git@github.com:LLNL/ddcMD.git:

    maintainers = ['XiaohuaZhangLLNL', 'bhatiaharsh']

    version('develop', branch='develop', submodules=True)

    depends_on('cmake', type='build')
    depends_on('mpi')
    depends_on('fftw')

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+cuda' in spec:
            args.append('-DUSE_GPU=ON')
        else:
            args.append('-DUSE_GPU=OFF')
        return args

    @run_after('install')
    def _fix_exename(self):

        # the executable is named as ddcMD_?PU_[host]
        # we want to rename it to ddcMD_?PU (i.e., remove the [host])
        new_name = 'ddcMD_GPU' if '+cuda' in self.spec else 'ddcMD_CPU'

        with working_dir(self.prefix.bin):
            files = os.listdir(os.getcwd())
            assert 1 == len(files)
            old_name = files[0]
            assert new_name == old_name[:len(new_name)]

            tty.info('Renaming installed executable from ({0}) to ({1})'.format(old_name, new_name))
            os.rename(old_name, new_name)

