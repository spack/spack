# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNibabel(PythonPackage):
    """Access a multitude of neuroimaging data formats"""

    homepage = "https://nipy.org/nibabel"
    pypi = "nibabel/nibabel-3.2.1.tar.gz"
    git = "https://github.com/nipy/nibabel"

    maintainers("ChristopherChristofi")

    # As detailed: https://nipy.org/nibabel/legal.html
    license("MIT AND BSD-3-Clause AND PSF-2.0 AND PDDL-1.0")

    version(
        "5.2.1",
        sha256="2cbbc22985f7f9d39d050df47249771dfb8d48447f5e7a993177e4cabfe047f0",
        url="https://pypi.org/packages/77/3f/ce43b8c2ccc4a7913a87c4d425aaf0080ea3abf947587e47dc2025981a17/nibabel-5.2.1-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="b3deb8130c835b9d26e80880b0d5e443d9e3f30972b3b0302dd2fafa3ca629f8",
        url="https://pypi.org/packages/9d/60/54aa4ec55ae7cacb8d7e3d18af2e0b55efb55852b3e0ef482113530d3929/nibabel-5.1.0-py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="c4fe76348aa865f8300beaaf2a69d31624964c861853ef80c06e33d5f244413c",
        url="https://pypi.org/packages/89/51/c97641cc2cd1b3b14cdec54b4e86fe03fc59753ecd13dc67544716fb7353/nibabel-4.0.2-py3-none-any.whl",
    )
    version(
        "3.2.2",
        sha256="7df7a2733461441d3aacc61f36f5e100ec533d43ed09a191293bb4ca5a4f10f6",
        url="https://pypi.org/packages/c3/f1/6e31b0287aed62233ec93535ac55554ec5e80c81b772b411e878c9d17179/nibabel-3.2.2-py3-none-any.whl",
    )
    version(
        "3.2.1",
        sha256="7e26cbf60eae8668785fa970294f05f767cefc5538b9e22aa388a07f62c54ebc",
        url="https://pypi.org/packages/42/bf/ba089fec67237f6439c345b8977ca6dde67402ada6592bf84c2c78d557ff/nibabel-3.2.1-py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="be0c8023cabee9073ccacca26ba7a296f0eb5d2fd24dfac2709fb7886a8d61ff",
        url="https://pypi.org/packages/66/30/fbed62172920c3fd050b6483541546a87c5e735f4a0ef03f08bb150680b4/nibabel-2.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5:")
        depends_on("python@3.7:", when="@4")
        depends_on("py-importlib-resources@1.3:", when="@5.1: ^python@:3.8")
        depends_on("py-numpy@1.20.0:", when="@5.2:")
        depends_on("py-numpy@1.19.0:", when="@5:5.1")
        depends_on("py-numpy@1.17.0:", when="@4")
        depends_on("py-numpy@1.14.0:", when="@3.2:3")
        depends_on("py-numpy@1.8:", when="@2.4:2.5.1")
        depends_on("py-packaging@17:", when="@4:")
        depends_on("py-packaging@14.3:", when="@3.1:3")
        depends_on("py-setuptools", when="@3.2.2:5.0")
        depends_on("py-six@1.3:", when="@2.3.3:2")

    # Historical dependencies
