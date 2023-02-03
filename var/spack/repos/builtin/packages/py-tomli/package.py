# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomli(Package, PythonExtension):
    """Tomli is a Python library for parsing TOML. Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/t/tomli/tomli-2.0.1-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tomli/"
    git = "https://github.com/hukkin/tomli.git"

    maintainers("charmoniumq")

    version(
        "2.0.1",
        sha256="939de3e7a6161af0c887ef91b7d41a53e7c5a1ca976325f429cb46ea9bc30ecc",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
