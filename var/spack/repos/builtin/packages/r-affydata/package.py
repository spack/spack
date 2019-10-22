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
    url      = "https://www.bioconductor.org/packages/release/data/experiment/src/contrib/affydata_1.32.0.tar.gz"

    version('1.32.0', sha256='059e05a2b8908720801d684d5617d5d5e45db7a5999c5659a22daf87658538d1')

    depends_on('r@3.4.0:3.4.9', when=('@1.24.0'))
    depends_on('r-affy', type=('build', 'run'))
