# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmocean(PythonPackage):
    """Colormaps for Oceanography."""

    homepage = "https://matplotlib.org/cmocean/"
    pypi = "cmocean/cmocean-2.0.tar.gz"

    license("MIT")

    version(
        "3.0.3",
        sha256="a23e4b7893e05dfd958931df53fc0e31bca09a572c13d78158a79ade47dc44bf",
        url="https://pypi.org/packages/eb/33/1b5353a244ea5b8b21e2324b3e00f4983b8f1b2f48f02b61379423e0d259/cmocean-3.0.3-py3-none-any.whl",
    )
    version(
        "2.0",
        sha256="1753f004d84d21c89e76106b2f56e2847808951b2373843bece4dcf532e1a91f",
        url="https://pypi.org/packages/48/02/d0f19b00b252fd972e3daec05be73aa811091528f21b90442a15d6a96d89/cmocean-2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3:")
        depends_on("py-matplotlib", when="@3:")
        depends_on("py-numpy", when="@3:")
        depends_on("py-packaging", when="@3:")
