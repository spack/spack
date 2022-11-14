# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtmlmin(PythonPackage):
    """An HTML Minifier."""

    pypi = "htmlmin/htmlmin-0.1.12.tar.gz"

    #maintainers = ["wscullin"]

    version("0.1.12", sha256="50c1ef4630374a5d723900096a961cff426dff46b48f34d194a81bbe14eca178")

    depends_on("py-setuptools", type="build")
