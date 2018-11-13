# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiomformat(RPackage):
    """This is an R package for interfacing with the BIOM format. This
    package includes basic tools for reading biom-format files, accessing
    and subsetting data tables from a biom object (which is more complex
    than a single table), as well as limited support for writing a
    biom-object back to a biom-format file. The design of this API is
    intended to match the python API and other tools included with the
    biom-format project, but with a decidedly "R flavor" that should be
    familiar to R users. This includes S4 classes and methods, as well
    as extensions of common core functions/methods."""

    homepage = "https://www.bioconductor.org/packages/biomformat/"
    git      = "https://git.bioconductor.org/packages/biomformat.git"

    version('1.4.0', commit='83b4b1883bc56ea93a0a6ca90fc1b18712ef0f1a')

    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rhdf5', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.0')
