# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RParamhelpers(RPackage):
    """Functions for parameter descriptions and operations in black-box
       optimization, tuning and machine learning. Parameters can be described
       (type, constraints, defaults, etc.), combined to parameter sets and can
       in general be programmed on. A useful OptPath object (archive) to log
       function evaluations is also provided."""

    homepage = "https://github.com/berndbischl/ParamHelpers"
    url      = "https://cran.r-project.org/src/contrib/ParamHelpers_1.10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ParamHelpers"

    version('1.10', '36e9060488ebd484d62cd991a4693332')

    depends_on('r-bbmisc@1.10:', type=('build', 'run'))
    depends_on('r-checkmate@1.8.1:', type=('build', 'run'))
