# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxDesign(PythonPackage):
    """A sphinx extension for designing beautiful, screen-size responsive web components."""

    homepage = "https://sphinx-design.readthedocs.io"
    pypi = "sphinx-design/sphinx_design-0.3.0.tar.gz"

    maintainers("ax3l", "adamjstewart")

    version("0.3.0", sha256="7183fa1fae55b37ef01bda5125a21ee841f5bbcbf59a35382be598180c4cefba")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.4:3", type=("build"))
    depends_on("py-sphinx@4:5", type=("build", "run"))
