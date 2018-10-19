# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRjsonio(RPackage):
    """This is a package that allows conversion to and from data in Javascript
    object notation (JSON) format. This allows R objects to be inserted into
    Javascript/ECMAScript/ActionScript code and allows R programmers to read
    and convert JSON content to R objects. This is an alternative to rjson
    package. Originally, that was too slow for converting large R objects to
    JSON and was not extensible. rjson's performance is now similar to this
    package, and perhaps slightly faster in some cases. This package uses
    methods and is readily extensible by defining methods for different
    classes, vectorized operations, and C code and callbacks to R functions for
    deserializing JSON objects to R. The two packages intentionally share the
    same basic interface. This package (RJSONIO) has many additional options to
    allow customizing the generation and processing of JSON content. This
    package uses libjson rather than implementing yet another JSON parser. The
    aim is to support other general projects by building on their work,
    providing feedback and benefit from their ongoing development."""

    homepage = "https://cran.r-project.org/package=RJSONIO"
    url      = "https://cran.r-project.org/src/contrib/RJSONIO_1.3-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RJSONIO"

    version('1.3-0', '72c395622ba8d1435ec43849fd32c830')
