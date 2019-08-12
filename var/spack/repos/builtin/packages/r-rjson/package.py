# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRjson(RPackage):
    """Converts R object into JSON objects and vice-versa."""

    homepage = "https://cran.r-project.org/package=rjson"
    url      = "https://cran.r-project.org/src/contrib/rjson_0.2.15.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rjson"

    version('0.2.15', '87d0e29bc179c6aeaf312b138089f8e9')
