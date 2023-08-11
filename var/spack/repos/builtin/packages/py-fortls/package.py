# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortls(PythonPackage):
    """A Language Server for Fortran providing code completion, diagnostics, hovering and more."""

    homepage = "https://fortls.fortran-lang.org"
    pypi = "fortls/fortls-2.13.0.tar.gz"

    maintainers("RMeli")

    version("2.13.0", sha256="23c5013e8dd8e1d65bf07be610d0827bc48aa7331a7a7ce13612d4c646d0db31")

    depends_on("py-setuptools@45:", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")

    depends_on("py-json5", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.7")
