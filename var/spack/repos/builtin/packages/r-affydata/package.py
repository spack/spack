# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffydata(RPackage):
    """Example datasets of a slightly large size. They represent 'real
    world examples', unlike the artificial examples included in the
    package affy."""

    homepage = "https://www.bioconductor.org/packages/affydata/"
    url      = "https://www.bioconductor.org/packages/release/data/experiment/src/contrib/affydata_1.24.0.tar.gz"

    version('1.24.0', '0b6938685c450a56d65dd5628ebed42d')

    depends_on('r@3.4.0:3.4.9', when=('@1.24.0'))
    depends_on('r-affy', type=('build', 'run'))
