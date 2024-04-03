# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPandasStubs(PythonPackage):
    """These are public type stubs for pandas, following the convention of
    providing stubs in a separate package, as specified in PEP 561. The stubs
    cover the most typical use cases of pandas. In general, these stubs are
    narrower than what is possibly allowed by pandas, but follow a convention of
    suggesting best recommended practices for using pandas."""

    homepage = "https://pandas.pydata.org/"
    pypi = "pandas_stubs/pandas_stubs-2.0.2.230605.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0.2.230605",
        sha256="39106b602f3cb6dc5f728b84e1b32bde6ecf41ee34ee714c66228009609fbada",
        url="https://pypi.org/packages/09/1d/2b9b5905d869c3e65d1c35e2a6420cbe4313a277aabfae6001670ef04075/pandas_stubs-2.0.2.230605-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2:2.0")
        depends_on("py-numpy@1.24.3:", when="@2.0.2")
        depends_on("py-types-pytz@2022.1.1:")
