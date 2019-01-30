# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMzid(RPackage):
    """A parser for mzIdentML files implemented using the XML package. The
       parser tries to be general and able to handle all types of mzIdentML
       files with the drawback of having less 'pretty' output than a vendor
       specific parser. Please contact the maintainer with any problems and
       supply an mzIdentML file so the problems can be fixed quickly."""

    homepage = "https://www.bioconductor.org/packages/mzID/"
    git      = "https://git.bioconductor.org/packages/mzID.git"

    version('1.14.0', commit='1c53aa6523ae61d3ebb13381381fc119d6cc6115')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
