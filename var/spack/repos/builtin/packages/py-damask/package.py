# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDamask(PythonPackage):
    """Pre- and post-processing tools for DAMASK"""

    homepage = "https://damask.mpie.de"
    url = "https://damask.mpie.de/download/damask-3.0.0.tar.xz"

    maintainers("MarDiehl")

    license("AGPL-3.0-or-later")

    version(
        "3.0.0-beta0",
        sha256="c6656c514268578dd5834ca402eeb7c58edc8bf73fa50106f462326b1c397482",
        url="https://pypi.org/packages/93/1b/38e4d84cdd0ae30818e761168b13f32bbb970c65eb301e215caf124a3ac0/damask-3.0.0b0-py3-none-any.whl",
    )
    version(
        "3.0.0-alpha8",
        sha256="8261d446cd423d91b6c7b01e487729cd0ddbf923b549c334b682608f3d15c832",
        url="https://pypi.org/packages/23/40/f9bc7bd9fa51494f643aef9afd2f356dcf634220dc90fba4910f2fbfae8b/damask-3.0.0a8-py3-none-any.whl",
    )
    version(
        "3.0.0-alpha7",
        sha256="af282fc66872d81809205c6f7d4acd8009118ac35768c1c251239b5fd858a592",
        url="https://pypi.org/packages/ba/74/10cd3c2c72789ce175dbc8f661d35db91e3e3ddb052143e0dbef1ad6f15b/damask-3.0.0a7-py3-none-any.whl",
    )
    version(
        "3.0.0-alpha6",
        sha256="80c2c5e8b7e573aa416b225789abdeb4fafb45c27dd58113b20d8b7dbb112b24",
        url="https://pypi.org/packages/d4/d3/1d1f0d0088f974e20bc1705219fbc01c62d846fefe841c77b605363612b5/damask-3.0.0a6-py3-none-any.whl",
    )
    version(
        "3.0.0-alpha5",
        sha256="ecb5016d94ca8b12cb5357768ac2049e9655af7a58286a08be1778dae93671cf",
        url="https://pypi.org/packages/f1/71/1374e4b7fdc8852542c5ab4d3c6e719d93e670f161e6bbbcc703e5444757/damask-3.0.0a5-py3-none-any.whl",
    )
    version(
        "3.0.0-alpha4",
        sha256="af693d391627983b84d97242b68334a7b227f2ae907b11d7d1268844fe24385a",
        url="https://pypi.org/packages/b4/43/a16318a70b274aa41cf3840cc43cf95fff214c665cded2b6fe8fa40e25b6/damask-3.0.0a4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py@2.9.0:", when="@3.0.0-alpha3:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-matplotlib@3.0.0:", when="@3.0.0-alpha3:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-numpy@1.17.0:", when="@3.0.0-alpha5:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-pandas@0.24.0:", when="@3.0.0-alpha3:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-pyaml", when="@3.0.0-alpha3:3.0.0-alpha4")
        depends_on("py-pyyaml", when="@3.0.0-alpha7 ^python@:3.12.0")
        depends_on("py-pyyaml@3.12:", when="@3.0.0-alpha5:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-scipy@1.2.0:", when="@3.0.0-alpha3:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-vtk@8.1:", when="@3.0.0-alpha3:3.0.0-alpha8,3.0.0-beta0:")
        depends_on("py-vtk", when="@:3.0.0-alpha2,3.0.0-alpha7,3.0.0-alpha678")

    patch("setup.patch", when="@3.0.0-alpha7")

    build_directory = "python"
