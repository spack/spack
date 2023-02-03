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

    version(
        "0.4.6",
        sha256="4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6",
        expand=False,
    )
    version(
        "0.4.5",
        sha256="854bf444933e37f5824ae7bfc1e98d5bce2ebe4160d46b5edf346a89358e99da",
        expand=False,
    )
    version(
        "0.4.4",
        sha256="9f47eda37229f68eee03b24b9748937c7dc3868f906e8ba69fbcbdd3bc5dc3e2",
        expand=False,
    )
    version(
        "0.4.1",
        sha256="f8ac84de7840f5b9c4e3347b3c1eaa50f7e49c2b07596221daec5edaabbd7c48",
        expand=False,
    )
    version(
        "0.3.7",
        sha256="a4c0f5bc358a62849653471e309dcc991223cf86abafbec17cd8f41327279e89",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
