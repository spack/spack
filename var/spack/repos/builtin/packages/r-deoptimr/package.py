# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeoptimr(RPackage):
    """An implementation of a bespoke jDE variant of the Differential
       Evolution stochastic algorithm for global optimization of
       nonlinear programming problems."""

    homepage = "https://cloud.r-project.org/package=DEoptimR"
    url      = "https://cloud.r-project.org/src/contrib/DEoptimR_1.0-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DEoptimR"

    version('1.0-8', 'c85836a504fbe4166e3c8eba0efe705d')
