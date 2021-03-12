# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Parallelmergetree(CMakePackage):
    """A multi-runtime implementation of a distributed merge tree
    segmentation algorithm. The implementation relies on the framework
    BabelFlow, which allows to execute the algorithm on different runtime
    systems."""

    homepage = "https://bitbucket.org/cedmav/parallelmergetree"
    git      = "https://bitbucket.org/cedmav/parallelmergetree.git"

    maintainers = ['spetruzza']

    version('1.0.0',
            git='https://bitbucket.org/cedmav/parallelmergetree.git',
            tag='v1.0.0',
            submodules=True)

    depends_on('babelflow')

    variant("shared", default=True, description="Build ParallelMergeTree as shared libs")

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DLIBRARY_ONLY=ON'
        ]
        return args
