# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jq(AutotoolsPackage):
    """jq is a lightweight and flexible command-line JSON processor."""

    homepage = "https://stedolan.github.io/jq/"
    url      = "https://github.com/stedolan/jq/archive/jq-1.5.tar.gz"

    version('1.5', 'c8070bd6ec275404f77db3d2e568c9a3')

    depends_on('oniguruma')
    depends_on('bison@3.0:', type='build')
