# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColoredTraceback(PythonPackage):
    """Automatically color Python's uncaught exception tracebacks."""

    homepage = "https://github.com/staticshock/colored-traceback.py"
    pypi = "colored-traceback/colored-traceback-0.3.0.tar.gz"

    license("ISC")

    version(
        "0.3.0",
        sha256="f76c21a4b4c72e9e09763d4d1b234afc469c88693152a763ad6786467ef9e79f",
        url="https://pypi.org/packages/68/95/d9b20efe099fff830502c6c7b83da4f1cdfd3346922d87da9bca3e63f897/colored_traceback-0.3.0-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pygments", when="@0.2.2:")
