# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCirclize(RPackage):
    """Circular layout is an efficient way for the visualization of huge
       amounts of information. Here this package provides an implementation
       of circular layout generation in R as well as an enhancement of
       available software. The flexibility of the package is based on the
       usage of low-level graphics functions such that self-defined
       high-level graphics can be easily implemented by users for specific
       purposes. Together with the seamless connection between the powerful
       computational and visual environment in R, it gives users more
       convenience and freedom to design figures for better understanding
       complex patterns behind multiple dimensional data."""

    homepage = "https://cloud.r-project.org/package=circlize"
    url      = "https://cloud.r-project.org/src/contrib/circlize_0.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/circlize"

    version('0.4.6', sha256='cec88cfc5e512a111cc37177552c25698ccc0e9bbecb0d6e60657e7b115a56fa')
    version('0.4.1', '6818830654f485abbdc8c74ec9087377')
    version('0.4.0', '0dbf1b481930a759d6f413d17f8ae1c4')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-globaloptions@0.1.0:', type=('build', 'run'))
    depends_on('r-shape', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
