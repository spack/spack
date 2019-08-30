# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertthat(RPackage):
    """assertthat is an extension to stopifnot() that makes it easy to declare
    the pre and post conditions that you code should satisfy, while also
    producing friendly error messages so that your users know what they've done
    wrong."""

    homepage = "https://cloud.r-project.org/package=assertthat"
    url      = "https://cloud.r-project.org/src/contrib/assertthat_0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertthat"

    version('0.2.1', sha256='85cf7fcc4753a8c86da9a6f454e46c2a58ffc70c4f47cac4d3e3bcefda2a9e9f')
    version('0.2.0', '8134f0072c6a84fd738d3bfc5e7f68ef')
    version('0.1', '59f9d7f7c00077ea54d763b78eeb5798')
