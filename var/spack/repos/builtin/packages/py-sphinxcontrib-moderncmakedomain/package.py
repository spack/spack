# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribModerncmakedomain(PythonPackage):
    """Sphinx Domain for Modern CMake."""

    homepage = "https://github.com/scikit-build/moderncmakedomain"
    pypi = "sphinxcontrib_moderncmakedomain/sphinxcontrib_moderncmakedomain-3.25.0.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version(
        "3.27.0",
        sha256="70a73e0e7cff1b117074e968ccb7f72383ed0f572414df0e216cea06914de988",
        url="https://pypi.org/packages/af/d7/67b518158634508c439eba83d7e5db4c3d6e87b7a0c8d2dd37b7a7b0bb98/sphinxcontrib_moderncmakedomain-3.27.0-py3-none-any.whl",
    )
    version(
        "3.26.4",
        sha256="45eb2463bf0b5767e6856dbb79a1ce901b526a92cf1b845d3f30399a80bae60e",
        url="https://pypi.org/packages/8d/53/7e88165aac128885ca7c86802667555178c0f835676dc50122a805160010/sphinxcontrib_moderncmakedomain-3.26.4-py3-none-any.whl",
    )
    version(
        "3.25.0",
        sha256="02cf07c5b6a0b42e237b01c6002cd42c2394cd66f63cfed19ea9d807107c2a97",
        url="https://pypi.org/packages/3d/a8/cad7deae4fab8428255a3e845bdec92075c365a54e54cde1658c6f03ca1e/sphinxcontrib_moderncmakedomain-3.25.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.26:")
        depends_on("py-sphinx@2.0.0:", when="@3.27:")
        depends_on("py-sphinx", when="@3.25:3.26")
