# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Memaxes(Package):
    """MemAxes is a visualizer for sampled memory trace data."""

    homepage = "https://github.com/llnl/MemAxes"

    version('0.5', '5874f3fda9fd2d313c0ff9684f915ab5',
            url='https://github.com/llnl/MemAxes/archive/v0.5.tar.gz')

    depends_on('cmake@2.8.9:', type='build')
    depends_on("qt@5:")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
