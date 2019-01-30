# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBindrcpp(RPackage):
    """Provides an easy way to fill an environment with active bindings that
       call a C++ function."""

    homepage = "https://github.com/krlmlr/bindrcpp"
    url      = "https://cran.r-project.org/src/contrib/bindrcpp_0.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bindrcpp"

    version('0.2.2', '48130709eba9d133679a0e959e49a7b14acbce4f47c1e15c4ab46bd9e48ae467')
    version('0.2', '2ed7f19fd9a12587f882d90060e7a343')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-bindr', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
