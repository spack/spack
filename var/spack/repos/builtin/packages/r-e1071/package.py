# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RE1071(RPackage):
    """Functions for latent class analysis, short time Fourier transform, fuzzy
    clustering, support vector machines, shortest path computation, bagged
    clustering, naive Bayes classifier, ..."""

    homepage = "https://cran.r-project.org/package=e1071"
    url      = "https://cran.r-project.org/src/contrib/e1071_1.6-7.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/e1071"

    version('1.7-1', sha256='5c5f04a51c1cd2c7dbdf69987adef9bc07116804c63992cd36d804a1daf89dfe')
    version('1.6-7', 'd109a7e3dd0c905d420e327a9a921f5a')

    depends_on('r-class', type=('build', 'run'))
