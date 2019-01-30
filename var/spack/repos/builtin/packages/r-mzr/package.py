# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMzr(RPackage):
    """mzR provides a unified API to the common file formats and parsers
       available for mass spectrometry data. It comes with a wrapper for the
       ISB random access parser for mass spectrometry mzXML, mzData and mzML
       files. The package contains the original code written by the ISB, and a
       subset of the proteowizard library for mzML and mzIdentML. The netCDF
       reading code has previously been used in XCMS."""

    homepage = "https://www.bioconductor.org/packages/mzR/"
    git      = "https://git.bioconductor.org/packages/mzR.git"

    version('2.10.0', commit='a6168b68e48c281e88de9647254a8db1e21df388')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('netcdf')
    depends_on('r@3.4.0:3.4.9', when='@2.10.0')
