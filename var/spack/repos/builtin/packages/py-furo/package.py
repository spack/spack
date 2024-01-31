# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme.."""

    homepage = "https://github.com/pradyunsg/furo"
    pypi = "furo/furo-2023.5.20.tar.gz"

    license("MIT")

    version("2023.9.10", sha256="5707530a476d2a63b8cad83b4f961f3739a69f4b058bcf38a03a39fa537195b2")
    version("2023.5.20", sha256="40e09fa17c6f4b22419d122e933089226dcdb59747b5b6c79363089827dea16f")

    depends_on("py-sphinx-theme-builder@0.2.0a10:", type="build")

    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-sphinx@6:7", type=("build", "run"))
    depends_on("py-sphinx-basic-ng", type=("build", "run"))
    depends_on("py-pygments@2.7:", type=("build", "run"))
