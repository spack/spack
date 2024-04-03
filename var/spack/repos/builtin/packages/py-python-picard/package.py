# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPicard(PythonPackage):
    """Preconditoned ICA for Real Data."""

    homepage = "https://pierreablin.github.io/picard/"
    pypi = "python-picard/python-picard-0.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.6",
        sha256="26c7928f7aba69011f1236bf35388a420088018350e840d2608031c5f338e0f7",
        url="https://pypi.org/packages/c6/39/23ee91bfcf542a0554dd69991f6a695102322e631174e6e65d309c17b370/python_picard-0.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numexpr", when="@0.4:")
        depends_on("py-numpy", when="@0.6:")
