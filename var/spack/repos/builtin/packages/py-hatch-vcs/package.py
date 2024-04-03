# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchVcs(PythonPackage):
    """Hatch plugin for versioning with your preferred VCS"""

    homepage = "https://github.com/ofek/hatch-vcs"
    pypi = "hatch_vcs/hatch_vcs-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="60ce59a3fa4664057e4a858b6a96ab0b9dec21bf8f562f836139315bb361be8c",
        url="https://pypi.org/packages/00/b1/90cc7881c2e870333eeafa6afb7b27de53418aad1ba5409ad331c96608a1/hatch_vcs-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="86432a0dd49acae0e69e14f285667693fcd31d9869ca21634520acc30d482f07",
        url="https://pypi.org/packages/7d/47/73ff0d30c4fa8b175db04a104a55dbe7d2050632262575efe02b8e2c8e2b/hatch_vcs-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3")
        depends_on("py-hatchling@1.1:", when="@0.3:")
        depends_on("py-hatchling@0.21:", when="@0.2")
        depends_on("py-setuptools-scm@6.4:")
