# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCommonmark(RPackage):
    """High Performance CommonMark and Github Markdown Rendering in R.

    The CommonMark specification defines a rationalized version of markdown
    syntax. This package uses the 'cmark' reference implementation for
    converting markdown text into various formats including html, latex and
    groff man. In addition it exposes the markdown parse tree in xml format.
    Also includes opt-in support for GFM extensions including tables,
    autolinks, and strikethrough text."""

    cran = "commonmark"

    version('1.7', sha256='d14a767a3ea9778d6165f44f980dd257423ca6043926e3cd8f664f7171f89108')
