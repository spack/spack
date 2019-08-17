# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRegistry(RPackage):
    """Provides a generic infrastructure for creating and using registries."""

    homepage = "https://cran.r-project.org/web/packages/registry/index.html"
    url      = "https://cran.r-project.org/src/contrib/registry_0.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/registry"

    version('0.3', '85345b334ec81eb3da6edcbb27c5f421')
