# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRematch(RPackage):
    """Match Regular Expressions with a Nicer 'API'.

    A small wrapper on 'regexpr' to extract the matches and captured groups
    from the match of a regular expression to a character vector."""

    cran = "rematch"

    version('1.0.1', sha256='a409dec978cd02914cdddfedc974d9b45bd2975a124d8870d52cfd7d37d47578')
