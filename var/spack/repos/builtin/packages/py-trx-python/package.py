# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrxPython(PythonPackage):
    """Experiments with new file format for tractography."""

    homepage = "https://tee-ar-ex.github.io/trx-python/"
    pypi = "trx-python/trx-python-0.2.9.tar.gz"

    maintainers("ChristopherChristofi")

    license("BSD-2-Clause")

    version(
        "0.2.9",
        sha256="234438b7f103c49768ab98e5f46e7b2624327065cd23fbfce5e681c32e8b4a3f",
        url="https://pypi.org/packages/23/55/1a0953ffa30078aac893bff6b4e5ac2942eb34201f7c4375433f3337540b/trx_python-0.2.9-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.2:")
        depends_on("py-deepdiff")
        depends_on("py-nibabel@5:", when="@0.2:")
        depends_on("py-numpy@1.22.0:", when="@0.2:")
        depends_on("py-setuptools-scm")
