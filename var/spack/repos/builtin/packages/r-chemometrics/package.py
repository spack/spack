# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RChemometrics(RPackage):
    """R companion to the book "Introduction to Multivariate Statistical Analysis
    in Chemometrics" written by K. Varmuza and P. Filzmoser (2009)."""

    homepage = "https://cloud.r-project.org/package=chemometrics"
    url      = "https://cloud.r-project.org/src/contrib/chemometrics_1.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/chemometrics"

    version('1.4.2', '8137b0ca4004add9cc2ea81d2c54427f')
    version('1.4.1', '1e5a89442bb4a61db0da884eedd74fc2')
    version('1.3.9', '2b619791896db1513ca3d714acb68af3')
    version('1.3.8', '7fad828bd094b5485fbf20bdf7d3d0d1')
    version('1.3.7', 'a9e2f32efb1545421dd96185fd849184')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-lars', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-som', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
