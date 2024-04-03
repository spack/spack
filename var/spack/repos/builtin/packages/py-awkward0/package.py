# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkward0(PythonPackage):
    """Manipulate arrays of complex data structures as easily as Numpy.

    Awkward Array is a pure Python+Numpy library for manipulating complex data
    structures as you would Numpy arrays."""

    homepage = "https://github.com/scikit-hep/awkward-0.x"
    pypi = "awkward0/awkward0-0.15.5.tar.gz"

    version(
        "0.15.5",
        sha256="5fdaa3b29ea2426665215478b9b9199e991da5ab1f1f2996dcbfe848e08a40a1",
        url="https://pypi.org/packages/9a/b3/376b258ea021eed2c9bdaa1011e0f7b25365157de472d9fae8a2443d9ff5/awkward0-0.15.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.13.1:")
