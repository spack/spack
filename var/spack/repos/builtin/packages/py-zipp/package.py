# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZipp(Package, PythonExtension):
    """Backport of pathlib-compatible object wrapper for zip files."""

    homepage = "https://github.com/jaraco/zipp"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/z/zipp/zipp-3.12.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/zipp/"

    version("3.12.0", sha256="9eb0a4c5feab9b08871db0d672745b53450d7f26992fd1e4653aa43345e97b86", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
