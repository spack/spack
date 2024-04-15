# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssutils(PythonPackage):
    """A CSS Cascading Style Sheets library for Python."""

    homepage = "https://github.com/jaraco/cssutils"
    pypi = "cssutils/cssutils-2.7.1.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version(
        "2.7.1",
        sha256="1e92e0d9dab2ec8af9f38d715393964ba533dc3beacab9b072511dfc241db775",
        url="https://pypi.org/packages/7a/4a/acc05aba9edb75bf016d9f57928f0bea5a33de2079fd09ca61baec79a6f2/cssutils-2.7.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.4:2.7")
        depends_on("py-importlib-metadata", when="^python@:3.7")
