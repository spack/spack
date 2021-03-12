# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Babelflow(CMakePackage):
    """BabelFlow is an Embedded Domain Specific Language to describe
       algorithms using a task graph abstraction which allows them to be
       executed on top of one of several available runtime systems."""

    homepage = "https://github.com/sci-visus/BabelFlow"
    git      = 'https://github.com/sci-visus/BabelFlow.git'

    maintainers = ['spetruzza']

    version('1.0.0',  sha256='4c4d7ddf60e25e8d3550c07875dba3e46e7c9e61b309cc47a409461b7ffa405e')

    depends_on('mpi')

    variant("shared", default=True, description="Build Babelflow as shared libs")

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF')]
        return args
