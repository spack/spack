# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RSm(RPackage):
    """Smoothing Methods for Nonparametric Regression and Density Estimation.

    This is software linked to the book 'Applied Smoothing Techniques for Data
    Analysis - The Kernel Approach with S-Plus Illustrations' Oxford University
    Press."""

    cran = "sm"

    version('2.2-5.7', sha256='2607a2cafc68d7e99005daf99e36f4a66eaf569ebb6b7500e962642cf58be80f')
    version('2.2-5.6', sha256='b890cd7ebe8ed711ab4a3792c204c4ecbe9e6ca1fd5bbc3925eba5833a839c30')
    version('2.2-5.5', sha256='43e212a14c364b98b10018b56fe0a619ccffe4bde1294e6c45b3eafe7caf82e7')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.1.0:', type=('build', 'run'))
