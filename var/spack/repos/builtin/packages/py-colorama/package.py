# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorama(Package, PythonExtension):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py2.py3/c/colorama/colorama-0.4.6-py2.py3-none-any.whl"
    list_url = "https://pypi.org/simple/colorama/"

    version("0.4.6", sha256="4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
