# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToml(Package, PythonExtension):
    """Python Library for Tom's Obvious, Minimal Language."""

    homepage = "https://github.com/uiri/toml.git"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py2.py3/t/toml/toml-0.10.2-py2.py3-none-any.whl"
    list_url = "https://pypi.org/simple/toml/"

    version("0.10.2", sha256="806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b", expand=False)
    version("0.10.0", sha256="235682dd292d5899d361a811df37e04a8828a5b1da3115886b73cf81ebc9100e", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
