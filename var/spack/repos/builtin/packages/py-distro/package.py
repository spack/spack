# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDistro(PythonPackage):
    """Distro - an OS platform information API."""

    homepage = "https://github.com/nir0s/distro"
    pypi = "distro/distro-1.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.8.0",
        sha256="99522ca3e365cac527b44bde033f64c6945d90eb9f769703caaec52b09bbd3ff",
        url="https://pypi.org/packages/f4/2c/c90a3adaf0ddb70afe193f5ebfb539612af57cffe677c3126be533df3098/distro-1.8.0-py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="d596311d707e692c2160c37807f83e3820c5d539d5a83e87cfb6babd8ba3a06b",
        url="https://pypi.org/packages/e1/54/d08d1ad53788515392bec14d2d6e8c410bffdc127780a9a4aa8e6854d502/distro-1.7.0-py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="c8713330ab31a034623a9515663ed87696700b55f04556b97c39cd261aa70dc7",
        url="https://pypi.org/packages/b3/8d/a0a5c389d76f90c766e956515d34c3408a1e18f60fbaa08221d1f6b87490/distro-1.6.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="df74eed763e18d10d0da624258524ae80486432cd17392d9c3d96f5e83cd2799",
        url="https://pypi.org/packages/25/b7/b3c4270a11414cb22c6352ebc7a83aaa3712043be29daa05018fd5a5c956/distro-1.5.0-py2.py3-none-any.whl",
    )
