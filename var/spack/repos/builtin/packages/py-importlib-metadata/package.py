# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibMetadata(Package, PythonExtension):
    """Read metadata from Python packages."""

    homepage = "https://github.com/python/importlib_metadata"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/i/importlib-metadata/importlib_metadata-6.0.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/importlib-metadata/"
    git = "https://github.com/python/importlib_metadata"

    version("6.0.0", sha256="7efb448ec9a5e313a57655d35aa54cd3e01b7e1fbcf72dce1bf06119420f5bad", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-zipp@0.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.4:", when="^python@:3.7", type=("build", "run"))

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
