# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXarrayTensorstore(PythonPackage):
    """Xarray-TensorStore is a small library that allows opening Zarr arrays into Xarray
    via TensorStore, instead of the standard Zarr-Python library.
    """

    homepage = "https://github.com/google/xarray-tensorstore"
    pypi = "xarray-tensorstore/xarray-tensorstore-0.1.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.1.1",
        sha256="e372b232a63b5064f65c2a71636c12a790643c700473aabd347e2a18a186040b",
        url="https://pypi.org/packages/56/62/463bfeb8b23524369ea585a2998325b0050006aa82ae4f1cf05a7b701bc9/xarray_tensorstore-0.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.10:")
        depends_on("py-numpy")
        depends_on("py-tensorstore")
        depends_on("py-xarray")
        depends_on("py-zarr")
