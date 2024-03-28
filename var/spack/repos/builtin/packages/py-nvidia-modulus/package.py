# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNvidiaModulus(PythonPackage):
    """A deep learning framework for AI-driven multi-physics systems."""

    homepage = "https://github.com/NVIDIA/modulus"
    url = "https://github.com/NVIDIA/modulus/archive/refs/tags/v0.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.0",
        sha256="d1714e8d4c7161c3c3dbbaae5a91f60d7e5b25b6378bdd263771596a1db81da6",
        url="https://pypi.org/packages/16/ed/8eecb92101ba6e6c9d7624fc619d4a5a8e1c685083bd0185a1562606a155/nvidia_modulus-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-certifi@2023.7:", when="@0.2.1:")
        depends_on("py-fsspec@2023:", when="@0.3:")
        depends_on("py-h5py@3.7:", when="@:0.2")
        depends_on("py-netcdf4@1.6.3:", when="@:0.2")
        depends_on("py-numpy@1.22.4:1.24", when="@0.3:")
        depends_on("py-nvidia-dali-cuda110@1:")
        depends_on("py-nvtx@0.2.8:", when="@0.5:")
        depends_on("py-pytest@6.0.0:", when="@:0.2")
        depends_on("py-pytz@2023.3:", when="@0.4:")
        depends_on("py-ruamel-yaml@0.17.22:", when="@0.2")
        depends_on("py-s3fs@2023.5:", when="@0.2:")
        depends_on("py-setuptools@67.6:")
        depends_on("py-torch@2:", when="@0.3:")
        depends_on("py-tqdm@4.60:", when="@0.5:")
        depends_on("py-treelib@1.2.5:", when="@0.5:")
        depends_on("py-xarray@2023:", when="@0.2:")
        depends_on("py-zarr@2.14.2:", when="@0.2:")
