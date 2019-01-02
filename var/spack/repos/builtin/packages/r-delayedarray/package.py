# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDelayedarray(RPackage):
    """Wrapping an array-like object (typically an on-disk object) in a
       DelayedArray object allows one to perform common array operations on it
       without loading the object in memory. In order to reduce memory usage
       and optimize performance, operations on the object are either delayed
       or executed using a block processing mechanism. Note that this also
       works on in-memory array-like objects like DataFrame objects (typically
       with Rle columns), Matrix objects, and ordinary arrays and data frames.
       Wrapping an array-like object (typically an on-disk object) in a
       DelayedArray object allows one to perform common array operations on it
       without loading the object in memory. In order to reduce memory usage
       and optimize performance, operations on the object are either delayed
       or executed using a block processing mechanism. Note that this also
       works on in-memory array-like objects like DataFrame objects (typically
       with Rle columns), Matrix objects, and ordinary arrays and data
       frames."""

    homepage = "https://bioconductor.org/packages/DelayedArray/"
    git      = "https://git.bioconductor.org/packages/DelayedArray.git"

    version('0.6.5', commit='7d1cb6477cb024c38bf1ee0c9155e010249ed94e')
    version('0.4.1', commit='ffe932ef8c255614340e4856fc6e0b44128a27a1')
    version('0.2.7', commit='909c2ce1665ebae2543172ead50abbe10bd42bc4')

    depends_on('r-biocparallel', when='@0.6.5:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@0.6.5', type=('build', 'run'))
    depends_on('r-s4vectors@0.14.3:', when='@0.2.7', type=('build', 'run'))
    depends_on('r-s4vectors@0.15.3:', when='@0.4.1', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.43:', when='@0.6.5', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.11.17:', when='@0.4.1:', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@0.2.7', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@0.6.5', type=('build', 'run'))
