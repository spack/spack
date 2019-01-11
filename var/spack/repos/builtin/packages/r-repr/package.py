# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRepr(RPackage):
    """String and binary representations of objects for several formats and
    mime types."""

    homepage = "https://github.com/IRkernel/repr"
    url      = "https://cran.r-project.org/src/contrib/repr_0.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/repr"

    version('0.9', 'db5ff74893063b492f684e42283070bd')
