# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    pypi = "isort/isort-4.2.15.tar.gz"

    license("MIT")

    version(
        "5.12.0",
        sha256="f84c2818376e66cf843d497486ea8fed8700b340f308f076c6fb1229dff318b6",
        url="https://pypi.org/packages/0a/63/4036ae70eea279c63e2304b91ee0ac182f467f24f86394ecfe726092340b/isort-5.12.0-py3-none-any.whl",
    )
    version(
        "5.11.5",
        sha256="ba1d72fb2595a01c7895a5128f9585a5cc4b6d395f1c8d514989b9a7eb2a8746",
        url="https://pypi.org/packages/5f/f6/c55db45970fbd14de6ab72082f1b8a143c3a69aa031c1e0dd4b9ecc8d496/isort-5.11.5-py3-none-any.whl",
    )
    version(
        "5.10.1",
        sha256="6f62d78e2f89b4500b080fe3a81690850cd254227f27f75c3a0c491a1f351ba7",
        url="https://pypi.org/packages/b8/5b/f18e227df38b94b4ee30d2502fd531bebac23946a2497e5595067a561274/isort-5.10.1-py3-none-any.whl",
    )
    version(
        "5.9.3",
        sha256="e17d6e2b81095c9db0a03a8025a957f334d6ea30b26f9ec70805411e5c7c81f2",
        url="https://pypi.org/packages/c4/1d/f4e03047d6767e35c1efb13a280c1ef8b88807230f902da4cfc431a9f602/isort-5.9.3-py3-none-any.whl",
    )
    version(
        "5.9.1",
        sha256="8e2c107091cfec7286bc0f68a547d0ba4c094d460b732075b6fba674f1035c0c",
        url="https://pypi.org/packages/b3/3f/4e39910865572d2ff209e601d9c1d15180ef1b735538a0c7bc2d15b63ac6/isort-5.9.1-py3-none-any.whl",
    )
    version(
        "4.3.20",
        sha256="f57abacd059dc3bd666258d1efb0377510a89777fda3e3274e3c01f7c03ae22d",
        url="https://pypi.org/packages/1c/d9/bf5848b376e441ff358a14b954476423eeeb8c9b78c10074b7f53ce2918d/isort-4.3.20-py2.py3-none-any.whl",
    )
    version(
        "4.2.15",
        sha256="cd5d3fc2c16006b567a17193edf4ed9830d9454cbeb5a42ac80b36ea00c23db4",
        url="https://pypi.org/packages/a9/83/ca1c7737c9a43a3e5bd2b9954add88700267801415310395d4191e5ff8e3/isort-4.2.15-py2.py3-none-any.whl",
    )

    variant("colors", default=False, description="Install colorama for --color support")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5.12:5")
        depends_on("python@3.7:", when="@5.11,6:")
        depends_on("python@:3", when="@5:5.10")
        depends_on("py-colorama@0.4.3:", when="@5.2.1:5.12,6:+colors")

    conflicts("python@3.6.0", when="@5:")

    # https://github.com/PyCQA/isort/issues/2077
    conflicts("^py-poetry-core@1.5:", when="@:5.11.4")
