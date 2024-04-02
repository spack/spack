# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorama(PythonPackage):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    pypi = "colorama/colorama-0.3.7.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.6",
        sha256="4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6",
        url="https://pypi.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl",
    )
    version(
        "0.4.5",
        sha256="854bf444933e37f5824ae7bfc1e98d5bce2ebe4160d46b5edf346a89358e99da",
        url="https://pypi.org/packages/77/8b/7550e87b2d308a1b711725dfaddc19c695f8c5fa413c640b2be01662f4e6/colorama-0.4.5-py2.py3-none-any.whl",
    )
    version(
        "0.4.4",
        sha256="9f47eda37229f68eee03b24b9748937c7dc3868f906e8ba69fbcbdd3bc5dc3e2",
        url="https://pypi.org/packages/44/98/5b86278fbbf250d239ae0ecb724f8572af1c91f4a11edf4d36a206189440/colorama-0.4.4-py2.py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="f8ac84de7840f5b9c4e3347b3c1eaa50f7e49c2b07596221daec5edaabbd7c48",
        url="https://pypi.org/packages/4f/a6/728666f39bfff1719fc94c481890b2106837da9318031f71a8424b662e12/colorama-0.4.1-py2.py3-none-any.whl",
    )
    version(
        "0.3.7",
        sha256="a4c0f5bc358a62849653471e309dcc991223cf86abafbec17cd8f41327279e89",
        url="https://pypi.org/packages/b7/8e/ddb32ddaabd431813e180ca224e844bab8ad42fbb47ee07553f0ec44cd86/colorama-0.3.7-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.4.6-rc1:")
