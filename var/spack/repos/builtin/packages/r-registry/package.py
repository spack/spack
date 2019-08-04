# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRegistry(RPackage):
    """Provides a generic infrastructure for creating and using registries."""

    homepage = "https://cloud.r-project.org/web/packages/registry/index.html"
    url      = "https://cloud.r-project.org/src/contrib/registry_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/registry"

    version('0.5-1', sha256='dfea36edb0a703ec57e111016789b47a1ba21d9c8ff30672555c81327a3372cc')
    version('0.5', sha256='5d8be59ba791987b2400e9e8eaaac614cd544c1aece785ec4782ea6d5ea00efb')
    version('0.3', '85345b334ec81eb3da6edcbb27c5f421')
