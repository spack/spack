# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightlyUtils(PythonPackage):
    """A utility package for lightly."""

    homepage = "https://www.lightly.ai/"
    pypi = "lightly_utils/lightly_utils-0.0.2.tar.gz"

    license("MIT")

    version(
        "0.0.2",
        sha256="57eaa99044bbdab428cc67cd336491096cd406c21b50f15ce51150c1a10843e9",
        url="https://pypi.org/packages/62/11/ff55b3f54440e604a589ae1fe6950bc1bf49b5aca1842bf4b3ab0b6f65cd/lightly_utils-0.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-pillow")
