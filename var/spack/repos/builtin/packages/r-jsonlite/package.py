# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RJsonlite(RPackage):
    """A fast JSON parser and generator optimized for statistical data and the
    web. Started out as a fork of 'RJSONIO', but has been completely rewritten
    in recent versions. The package offers flexible, robust, high performance
    tools for working with JSON in R and is particularly powerful for building
    pipelines and interacting with a web API. The implementation is based on
    the mapping described in the vignette (Ooms, 2014). In addition to
    converting JSON data from/to R objects, 'jsonlite' contains functions to
    stream, validate, and prettify JSON data. The unit tests included with the
    package verify that all edge cases are encoded and decoded consistently for
    use with dynamic data in systems and applications."""

    homepage = "https://github.com/jeroenooms/jsonlite"
    url      = "https://cloud.r-project.org/src/contrib/jsonlite_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/jsonlite"

    version('1.6', sha256='88c5b425229966b7409145a6cabc72db9ed04f8c37ee95901af0146bb285db53')
    version('1.5', '2a81c261a702fccbbd5d2b32df108f76')
    version('1.2', '80cd2678ae77254be470f5931db71c51')
    version('1.0', 'c8524e086de22ab39b8ac8000220cc87')
    version('0.9.21', '4fc382747f88a79ff0718a0d06bed45d')
