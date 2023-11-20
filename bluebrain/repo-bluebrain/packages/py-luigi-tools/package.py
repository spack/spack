# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLuigiTools(PythonPackage):
    """Tools to work with luigi."""

    homepage = "https://github.com/BlueBrain/luigi-tools"
    pypi = "luigi-tools/luigi-tools-0.3.4.tar.gz"

    version("0.3.4", sha256="a249be5cda54fdde5bc18dc32b21a1c6096e742ffc1d36bd2b5b58dff5f9c131")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-setuptools-scm", type=("build"))

    depends_on("py-luigi", type="run")
    depends_on("py-jsonschema", type="run")
    depends_on("py-typing-extensions", type="run")
