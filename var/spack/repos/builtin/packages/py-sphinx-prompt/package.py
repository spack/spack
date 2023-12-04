# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxPrompt(PythonPackage):
    """Sphinx directive to add unselectable prompt."""

    homepage = "https://github.com/sbrunner/sphinx-prompt"
    pypi = "sphinx_prompt/sphinx_prompt-1.8.0.tar.gz"

    maintainers("LydDeb")

    version("1.8.0", sha256="47482f86fcec29662fdfd23e7c04ef03582714195d01f5d565403320084372ed")

    depends_on("python@3.9:3.11", type=("build","run"))
    depends_on("py-poetry@1.6", type=("build","run"))
    depends_on("py-poetry-core@1.0.0:", type="build")
    depends_on("py-poetry-plugin-tweak-dependencies-version", type="build")
    depends_on("py-poetry-dynamic-versioning", type="build")
    depends_on("py-sphinx@7.2.5", type=("build", "run"))
    depends_on("py-pygments@2.16.1", type=("build", "run"))
    depends_on("py-docutils@0.20.1", type=("build", "run"))
