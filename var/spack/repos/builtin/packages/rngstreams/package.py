# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rngstreams(AutotoolsPackage):
    """Multiple independent streams of pseudo-random numbers."""

    homepage = "http://statmath.wu.ac.at/software/RngStreams"
    url      = "http://statmath.wu.ac.at/software/RngStreams/rngstreams-1.0.1.tar.gz"

    version('1.0.1', '6d9d842247cd1d4e9e60440406858a69')
