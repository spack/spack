# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeekpath(PythonPackage):
    """SeeK-path is a python module to obtain band paths in the Brillouin zone of crystal
    structures."""

    homepage = "http://github.com/giovannipizzi/seekpath"
    pypi = "seekpath/seekpath-2.0.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "2.0.1",
        sha256="0fa50d3bd89bc1fac6bde8185a33a59d6994d53f2e7d1a0d1115fc0906ba012a",
        url="https://pypi.org/packages/1e/32/a8a8a421a769719286d6aadd14065e0324a1f2e32d106be31deed588ccb5/seekpath-2.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-spglib@1.14.1:", when="@1.9.2:")
