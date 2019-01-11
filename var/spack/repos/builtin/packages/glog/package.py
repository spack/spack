# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glog(Package):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url      = "https://github.com/google/glog/archive/v0.3.5.tar.gz"

    version('0.3.5', '5df6d78b81e51b90ac0ecd7ed932b0d4')
    version('0.3.4', 'df92e05c9d02504fb96674bc776a41cb')
    version('0.3.3', 'c1f86af27bd9c73186730aa957607ed0')

    depends_on('gflags')
    depends_on('cmake', when="@0.3.5:")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    @when('@0.3.5:')
    def install(self, spec, prefix):
        cmake_args = ['-DBUILD_SHARED_LIBS=TRUE']
        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')
