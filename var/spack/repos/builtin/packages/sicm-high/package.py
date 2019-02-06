# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SicmHigh(CMakePackage):
    """SICM's high-level interface. Seeks to automatically 
    profile and manage memory usage on heterogeneous memory systems."""

    homepage = "https://github.com/lanl/SICM/"
    git      = "https://github.com/lanl/SICM"

    version('develop', commit='HEAD')

    depends_on('flang@20180921', patches=['0.patch', '1.patch', '2.patch', '3.patch'])
    depends_on('jemalloc@5.1.0+je', patches=['jemalloc_maxarenas1.patch', 'jemalloc_maxarenas2.patch'])
    depends_on('numactl')
    depends_on('libpfm4')

    def cmake_args(self):
        args = ['-DSICM_BUILD_HIGH_LEVEL=True']
        return args

    # Run "make test" after the install target.
    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make("test")
