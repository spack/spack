# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSegmented(RPackage):
    """Given a regression model, segmented 'updates' the model by adding
    one or more segmented (i.e., piecewise-linear) relationships. Several
    variables with multiple breakpoints are allowed."""

    homepage = "https://cloud.r-project.org/package=segmented"
    url      = "https://cloud.r-project.org/src/contrib/segmented_0.5-1.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/segmented"

    version('1.0-0', sha256='eeadc89b4bb4744bbd1e4e6c3b6536ff96fc7ee09016228dfdc0a8ebdc74fac5')
    version('0.5-4.0', sha256='7ff63a19915cbd1e190d3a4875892b4c7bd97890b0dc2909126348a19aec4071')
    version('0.5-2.2', '1511ec365aea289d5f0a574f6d10d2d6')
    version('0.5-1.4', 'f9d76ea9e22ef5f40aa126b697351cae')
