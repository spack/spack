# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGcovr(PythonPackage):
    """Gcovr provides a utility for managing the use of the GNU gcov utility
    and generating summarized code coverage results. This command is inspired
    by the Python coverage.py package, which provides a similar utility for
    Python."""

    homepage = "https://gcovr.com/"
    pypi = "gcovr/gcovr-4.2.tar.gz"

    version(
        "5.2",
        sha256="16e2dbf67a4259cb17f520be3a251e9af605b94c1007b1419d8b55c5c6cf4c57",
        url="https://pypi.org/packages/f1/f1/1a9b50bb8899e485aa26805de2d8234df7e87d385685a6ab6e1aa36a0bac/gcovr-5.2-py2.py3-none-any.whl",
    )
    version(
        "4.2",
        sha256="9a4d1c23719f9ea217332d7aa8f9d109152aeecb7d6bfeab67ccc682994b9614",
        url="https://pypi.org/packages/70/8e/55232768ba46ba2cbb10ea04f3a8cf41540ee058a4e8eb5e3ac53d190e95/gcovr-4.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@5.1:6")
        depends_on("py-jinja2", when="@4:")
        depends_on("py-lxml", when="@4.2:")
        depends_on("py-pygments", when="@5:6")
