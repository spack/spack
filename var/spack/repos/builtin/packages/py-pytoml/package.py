# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytoml(Package, PythonExtension):
    """A parser for TOML-0.4.0.

    Deprecated: use py-toml instead."""

    homepage = "https://github.com/avakar/pytoml"
    url = "https://files.pythonhosted.org/packages/py2.py3/p/pytoml/pytoml-0.1.21-py2.py3-none-any.whl"
    list_url = "https://pypi.org/simple/pytoml/"

    version("0.1.21", sha256="57a21e6347049f73bfb62011ff34cd72774c031b9828cb628a752225136dfc33", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
