# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebcolors(PythonPackage):
    """Working with color names and values formats defined by HTML and CSS."""

    homepage = "https://pypi.org/project/webcolors/"
    pypi = "webcolors/webcolors-1.11.1.tar.gz"

    license("BSD-3-Clause")

    version("1.11.1", sha256="76f360636957d1c976db7466bc71dcb713bb95ac8911944dffc55c01cb516de6")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
