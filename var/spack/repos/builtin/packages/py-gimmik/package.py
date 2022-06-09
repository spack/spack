# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyGimmik(PythonPackage):
    """Generator of Matrix Multiplication Kernels - GiMMiK - is a tool for generation of
    high performance matrix multiplication kernel code.
    for various accelerator platforms."""

    homepage = "https://github.com/PyFR/GiMMiK"
    pypi = "gimmik/gimmik-2.2.tar.gz"

    maintainers = ["michaellaufer"]

    version(
        "2.2", sha256="9144640f94aab92f9c5dfcaf16885a79428ab97337cf503a4b2dddeb870f3cf0"
    )

    depends_on('python@3.8:', type=('build', 'run'))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=('build', 'run'))
    depends_on("py-mako", type=('build', 'run'))
