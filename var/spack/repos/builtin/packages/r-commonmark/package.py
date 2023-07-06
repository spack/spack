# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCommonmark(RPackage):
    """High Performance CommonMark and Github Markdown Rendering in R.

    The CommonMark specification defines a rationalized version of markdown
    syntax. This package uses the 'cmark' reference implementation for
    converting markdown text into various formats including html, latex and
    groff man. In addition it exposes the markdown parse tree in xml format.
    Also includes opt-in support for GFM extensions including tables,
    autolinks, and strikethrough text."""

    cran = "commonmark"

    version("1.9.0", sha256="6dd01a5a26c8d436486abf69c2f6ad0f8dd1c811f575c31983aeb4dbd376548f")
    version("1.8.1", sha256="96adcb093de3d2e48811af402da70e7222a313b97f1e979e0cbe84dd59bd5cbe")
    version("1.8.0", sha256="7d07e72937b1cf158e69f183722bf79dbb91b8967a9dd29f4fa145500c2be668")
    version("1.7", sha256="d14a767a3ea9778d6165f44f980dd257423ca6043926e3cd8f664f7171f89108")
