# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class PyNvidiaDali(PythonPackage):
    """A GPU-accelerated library containing highly optimized building blocks and
    an execution engine for data processing to accelerate deep learning training
    and inference applications."""

    homepage = "https://developer.nvidia.com/dali"
    url = "https://developer.download.nvidia.com/compute/redist/"

    maintainers("thomas-bouvier")

    system = platform.system().lower()
    arch = platform.machine()
    if "linux" in system and arch == "x86_64":
        version(
            "1.22.0-cuda120",
            sha256="6cbd9e3139d4c203f61f960f5ad1fc4b461621a60b7fa7ef0ba6d77c780b35f4",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.22.0-6971317-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.22.0-cuda110",
            sha256="8c3ccc7eddc1f63d3f858448c5c384ab129273e0c140e091aca2a98d48c5a80c",
            expand=False,
            preferred=True,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.22.0-6988993-py3-none-manylinux2014_x86_64.whl",
        )
    elif "linux" in system and arch == "aarch64":
        version(
            "1.22.0-cuda120",
            sha256="5e496eebeba3bc1cddd18e081c8c45121283478931cbe9b64912d2394d0942ca",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.22.0-6971317-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.22.0-cuda110",
            sha256="0da47629fec01abf418fda0eeb393998820e40f6fae6b4c7d3e625aa4cdba6bd",
            expand=False,
            preferred=True,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.22.0-6988993-py3-none-manylinux2014_aarch64.whl",
        )

    depends_on("python@3.6:3.10", type=("build", "run"))
    depends_on("cuda@12", when="@1.22.0-cuda120", type=("build", "run"))
    depends_on("cuda@11", when="@1.22.0-cuda110", type=("build", "run"))
    depends_on("py-astunparse@1.6.0:", type=("build", "run"))
    depends_on("py-gast@0.2.1:0.4.0", type=("build", "run"))
