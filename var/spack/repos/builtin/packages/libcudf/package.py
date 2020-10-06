# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcudf(CMakePackage):
    """Built based on the Apache Arrow columnar memory format,
    cuDF is a GPU DataFrame library for loading, joining,
    aggregating, filtering, and otherwise manipulating data."""

    homepage = "https://rapids.ai"
    url      = "https://github.com/rapidsai/cudf/archive/v0.15.0.tar.gz"

    version('0.15.0',  sha256='57b8036134368daa8a967eae971ee121cdc58c8678a03eba1358ed2b927dc16e')

    depends_on('cmake@3.14:', type='build')
    depends_on('cuda@10.0:')
    depends_on('boost')
    depends_on('arrow+cuda+orc')
    depends_on('librmm')
    depends_on('dlpack')

    root_cmakelists_dir = 'cpp'

    def cmake_args(self):
        args = []

        # args.append('-DGPU_ARCHES')
        args.append('-DUSE_NVTX=ON')
        args.append('-DBUILD_BENCHMARKS=OFF')
        args.append('-DDISABLE_DEPRICATION_WARNING=ON')
        args.append('-DPER_THREAD_DEFAULT_STREAM=OFF')
        return args
