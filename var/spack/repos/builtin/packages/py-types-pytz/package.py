# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPytz(PythonPackage):
    """This is a PEP 561 type stub package for the pytz package. It can be used
    by type-checking tools like mypy, pyright, pytype, PyCharm, etc. to check
    code that uses pytz."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-pytz/types-pytz-2023.3.0.0.tar.gz"

    version(
        "2023.3.0.0",
        sha256="4fc2a7fbbc315f0b6630e0b899fd6c743705abe1094d007b0e612d10da15e0f3",
        url="https://pypi.org/packages/84/69/cd7391875e53fe4d108f53417af51fb1720f3a48b30263db524aaf3e8141/types_pytz-2023.3.0.0-py3-none-any.whl",
    )
