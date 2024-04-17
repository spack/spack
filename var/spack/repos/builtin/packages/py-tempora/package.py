# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTempora(PythonPackage):
    """Objects and routines pertaining to date and time (tempora)"""

    homepage = "https://github.com/jaraco/tempora"
    pypi = "tempora/tempora-1.14.1.tar.gz"

    license("MIT")

    version(
        "1.14.1",
        sha256="d28a03d2f64ee81aec6e6bff374127ef306fe00c1b7e27c7ff1618344221a699",
        url="https://pypi.org/packages/5c/12/4c97c44e5c9d111649e363353a4ca3ece9c6cc04b11cc48540f26e42d7b9/tempora-1.14.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-jaraco-functools@1.20:", when="@1.13:5.1,5.2.1:")
        depends_on("py-pytz")
        depends_on("py-six", when="@:1")
