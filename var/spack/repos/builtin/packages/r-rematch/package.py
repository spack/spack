# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRematch(RPackage):
    """A small wrapper on 'regexpr' to extract the matches and
    captured groups from the match of a regular expression to a
    character vector."""

    homepage = "https://cloud.r-project.org/package=rematch"
    url      = "https://cloud.r-project.org/src/contrib/rematch_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rematch"

    version('1.0.1', '5271666295e232931f21499522489dd3')
