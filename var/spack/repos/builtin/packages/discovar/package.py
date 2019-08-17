# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Discovar(AutotoolsPackage):
    """DISCOVAR is a variant caller and small genome assembler."""

    homepage = "https://software.broadinstitute.org/software/discovar/blog/"
    url      = "ftp://ftp.broadinstitute.org/pub/crd/Discovar/latest_source_code/discovar-52488.tar.gz"

    version('52488', 'e72a0b9363e25c99d8e8729c0be98364')

    conflicts('%gcc@6:')
