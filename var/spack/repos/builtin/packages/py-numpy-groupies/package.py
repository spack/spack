# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpyGroupies(PythonPackage):
    """This package consists of a couple of optimised tools for doing things
    that can roughly be considered "group-indexing operations". The most
    prominent tool is `aggregate`. `aggregate` takes an array of values, and
    an array giving the group number for each of those values. It then returns
    the sum (or mean, or std, or any, ...etc.) of the values in each group.
    You have probably come across this idea before, using `matlab` accumarray,
    `pandas` groupby, or generally MapReduce algorithms and histograms. There
    are different implementations of `aggregate` provided, based on plain
    `numpy`, `numba` and `weave`. Performance is a main concern, and so far we
    comfortably beat similar implementations in other packages (check the
    benchmarks)."""

    homepage = "https://github.com/ml31415/numpy-groupies"
    pypi = "numpy_groupies/numpy_groupies-0.9.20.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.9.20",
        sha256="43c29c8f9fff5e2449a356c352bec0a5bb1a229c4e5b3281641ab04f9b864e8e",
        url="https://pypi.org/packages/e0/f1/0541f72a6052ad45af1c89f1393b2b7416be50ac549cb5f5e198a9ee8a89/numpy_groupies-0.9.20-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-numpy", when="@0.9.19:0.9.20,0.10:")
