# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWheyPth(PythonPackage):
    """Extension to whey to support .pth files."""

    homepage = "https://github.com/repo-helper/whey-pth"
    pypi = "whey-pth/whey-pth-0.0.5.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "0.0.5",
        sha256="452e8fe6493fc376ddd32a0a6991c046a5f7d000745b7e8defb307ed1837216c",
        url="https://pypi.org/packages/70/7b/95c2a0e7f59324d68dedea1aed8bddf84716fb44dbe9921ad26492ad91dc/whey_pth-0.0.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dom-toml@0.4:", when="@0.0.4:")
        depends_on("py-whey@0.0.15:", when="@0.0.4:")
