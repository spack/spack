# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RErgm(RPackage):
    """Fit, Simulate and Diagnose Exponential-Family Models for Networks.

    An integrated set of tools to analyze and simulate networks based on
    exponential-family random graph models (ERGMs). 'ergm' is a part of the
    Statnet suite of packages for network analysis. See Hunter, Handcock,
    Butts, Goodreau, and Morris (2008) <doi:10.18637/jss.v024.i03> and
    Krivitsky, Hunter, Morris, and Klumb (2021) <arXiv:2106.04997>."""

    cran = "ergm"

    version('4.1.2', sha256='1abc6ef53376a4132530c376ce477ae7a2590e95fe8feb011c0da9cfb4d49ba0')
    version('3.11.0', sha256='4e5506b44badc2343be3657acbf2bca51b47d7c187ff499d5a5e70a9811fe9f2')
    version('3.10.4', sha256='885f0b1a23c5a2c1947962350cfab66683dfdfd1db173c115e90396d00831f22')
    version('3.10.1', sha256='a2ac249ff07ba55b3359242f20389a892543b4fff5956d74143d2d41fa6d4beb')
    version('3.7.1', sha256='91dd011953b93ecb2b84bb3ababe7bddae25d9d86e69337156effd1da84b54c3')

    depends_on('r@3.5:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-network@1.15:', type=('build', 'run'))
    depends_on('r-network@1.17:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-robustbase@0.93-5:', type=('build', 'run'))
    depends_on('r-robustbase@0.93-7:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-coda@0.19-2:', type=('build', 'run'))
    depends_on('r-coda@0.19-4:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-trust@0.1.7:', type=('build', 'run'))
    depends_on('r-trust@0.1.8:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-matrix@1.2-17:', type=('build', 'run'))
    depends_on('r-matrix@1.3.2:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-lpsolveapi@5.5.2.0.17.7:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-mass@7.3-51.4:', type=('build', 'run'))
    depends_on('r-mass@7.3.53.1:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-statnet-common@4.3.0:', type=('build', 'run'))
    depends_on('r-statnet-common@4.4.0:', type=('build', 'run'), when='@3.11.0:')
    depends_on('r-statnet-common@4.5.0:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-rle', type=('build', 'run'), when='@3.11.0:')
    depends_on('r-rle@0.9.2:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-purrr@0.3.2:', type=('build', 'run'), when='@3.10.0:')
    depends_on('r-purrr@0.3.4:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-rlang@0.3.4:', type=('build', 'run'), when='@3.10.0:')
    depends_on('r-rlang@0.4.10:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-memoise@2.0.0:', type=('build', 'run'), when='@4.1.2:')
    depends_on('r-tibble@2.1.1:', type=('build', 'run'), when='@3.10.0:')
    depends_on('r-tibble@3.1.0:', type=('build', 'run'), when='@4.1.2:')

    depends_on('r-dplyr@0.8.0.1:', type=('build', 'run'), when='@3.10.0:3.10.4')
    depends_on('r-lpsolve@5.6.13:', type=('build', 'run'), when='@:3.11.0')

    # The CRAN page list OpenMPI as a dependency but this is not a dependency
    # for using the package. If one wishes to use MPI, simply load an MPI
    # package, along with r-dosnow and r-rmpi when using r-ergm, and set the
    # appropriate options in the R script.
