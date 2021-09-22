# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DependsAndConflictsWithExactVersions(Package):
    """
    This package is used to test whether the concretizer interprets the version
    3.0 in conflicts('mpich@3.0') and depends_on('mpich@3.0') as the closed-open
    range [3.0, 3.1). This is relevant for packages like mpich which have a
    versioning scheme that goes 3.0, 3.0.1, 3.0.2, ..., and 3.0 can be
    ambiguous, as mpich@3.0.1 satisfies mpich@3.0 as spec.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    variant('type', values=(
        'depends_on_3.0',
        'conflicts_with_3.0',
        'depends_on_3.0:3.0.0',
        'conflicts_with_3.0:3.0.0',
    ), multi=False, default='depends_on_3.0')

    depends_on('mpich')

    depends_on('mpich@3.0', when='type=depends_on_3.0')
    conflicts('^mpich@3.0', when='type=conflicts_with_3.0')
    depends_on('mpich@3.0:3.0.0', when='type=depends_on_3.0:3.0.0')
    conflicts('^mpich@3.0:3.0.0', when='type=conflicts_with_3.0:3.0.0')
