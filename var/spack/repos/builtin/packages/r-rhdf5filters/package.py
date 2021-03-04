# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import archspec
from spack import *


class RRhdf5filters(RPackage):
    """HDF5 Compression Filters

    Provides a collection of compression filters for use with HDF5 datasets."""

    homepage = "https://github.com/grimbough/rhdf5filters"
    git      = "https://git.bioconductor.org/packages/rhdf5filters"

    version('1.2.0', commit='25af0180f926b4b3ea11b30ec9277d26ad3d56b3')

    depends_on('r-rhdf5lib', type=('build', 'run'))
    depends_on('gmake', type='build')

    for t in set([str(x.family) for x in archspec.cpu.TARGETS.values()
                 if str(x.family) != 'x86_64']):
        conflicts('target={0}:'.format(t), msg='r-rhdf5filters is available x86_64 only')
