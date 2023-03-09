# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLuigiTools(PythonPackage):
    """Tools to work with luigi."""

    homepage = "https://github.com/BlueBrain/luigi-tools"
    pypi = "luigi-tools/luigi-tools-0.3.2.tar.gz"

    version("0.3.2", sha256="d408f3a742c74c0e41b4ca88cbd08ecb96d70a897fe35eb1c206cb6b67e9d745")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-setuptools-scm", type=("build"))

    depends_on("py-luigi", type="run")
    depends_on("py-jsonschema", type="run")
    depends_on("py-typing-extensions", type="run")
