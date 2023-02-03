# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPackaging(Package, PythonExtension):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/p/packaging/packaging-23.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/packaging/"

    version("23.0", sha256="714ac14496c3e68c99c29b00845f7a2b85f3bb6f1078fd9f72fd20f0570002b2", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
