# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEditables(PythonPackage):
    """A Python library for creating "editable wheels"."""

    homepage = "https://github.com/pfmoore/editables"
    pypi = "editables/editables-0.3.tar.gz"

    version("0.3", sha256="167524e377358ed1f1374e61c268f0d7a4bf7dbd046c656f7b410cde16161b1a")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
