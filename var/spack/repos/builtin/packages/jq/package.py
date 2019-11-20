# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jq(AutotoolsPackage):
    """jq is a lightweight and flexible command-line JSON processor."""

    homepage = "https://stedolan.github.io/jq/"
    url      = "https://github.com/stedolan/jq/archive/jq-1.5.tar.gz"

    version('1.5', sha256='d5667641d28c27d0c1e70de83e7f9bd8b2fed7fbf6a1d68731177d400a533c65')

    depends_on('oniguruma')
    depends_on('bison@3.0:', type='build')
