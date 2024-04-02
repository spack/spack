# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestDoctestplus(PythonPackage):
    """Pytest plugin with advanced doctest features."""

    homepage = "https://github.com/astropy/pytest-doctestplus"
    pypi = "pytest-doctestplus/pytest-doctestplus-0.8.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.13.0",
        sha256="a2809d8b6faadc7f909013b52e1ad36ae6b5371a0393ee8d05bc5719868b3f7a",
        url="https://pypi.org/packages/d5/f1/95cbe47ec92b4945536f151789624dbaece4beed6b2c1feba4abf62d79e8/pytest_doctestplus-0.13.0-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="66859d3c3d73793274803a91b4cb9912d1a7baf5c883e92859f2dfe11b35a631",
        url="https://pypi.org/packages/c3/a1/d25d7cd9eb48d78c54c24ded2d8338aead358e6e53a99f9324a31a4f9fa8/pytest_doctestplus-0.9.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.10:1.0")
        depends_on("py-packaging@17:", when="@0.10:")
        depends_on("py-pytest@4.6:", when="@0.9:")
        depends_on("py-setuptools@30.3:", when="@0.9:")
