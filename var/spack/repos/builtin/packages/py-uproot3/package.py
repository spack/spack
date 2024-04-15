# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot3(PythonPackage):
    """ROOT I/O in pure Python and Numpy.

    uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://github.com/scikit-hep/uproot3"
    pypi = "uproot3/uproot3-3.14.4.tar.gz"

    version(
        "3.14.4",
        sha256="d0b513aed4af17278d582a4879eff7037efe0752c7e2154683ac4c4f083c30c0",
        url="https://pypi.org/packages/9c/69/d893c6eba0dd0d8f82d841d4b85b6e63c52a1b472aec7cf7ae0efedf5a92/uproot3-3.14.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-awkward0")
        depends_on("py-cachetools")
        depends_on("py-numpy@1.13.1:")
        depends_on("py-uproot3-methods", when="@3.14.1:")
