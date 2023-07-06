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
            "1.27.0-cuda120",
            sha256="d8def4361bd9f888ddac3e2316b9eb89ee216f280c0973be12b8e1061d1ff108",
            expand=False,
            preferred=True,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.27.0-8625314-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.27.0-cuda110",
            sha256="9edf5097787cb1bbbbabc291d814bf367c5f5a986cffa101205fe31c86418a66",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.27.0-8625303-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.26.0-cuda120",
            sha256="784dbad4e4e1399b4d2f51bfa1a01e3e23f6fb37e8f327cf136df9c1b5fb8470",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.26.0-8269288-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.26.0-cuda110",
            sha256="545b56c104def627d6c2ead747875eaadba2e12610850b4480f718dc3e8a9177",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.26.0-8269290-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.25.0-cuda120",
            sha256="72591f0db9fe6dd82035b2b6cc41aed478e48656ba99e81344a9cb59123710aa",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.25.0-7922358-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.25.0-cuda110",
            sha256="9901cfa0f67674e5d2b77dbd90d3506b42390d12fc5996593fd395c0370ea46f",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.25.0-7922357-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.24.0-cuda120",
            sha256="f280fba3e917a0c47e705fa488c6d53e5c50629b3664fe6cf95d0913213f3b13",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.24.0-7582307-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.24.0-cuda110",
            sha256="5988317a5f17fdefa9254bebb6f8dc344c2b0bd958badf6688172e537d324d60",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.24.0-7582302-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.23.0-cuda120",
            sha256="d10a14074df6cdd38adb1181785372ab8ace677323fdf62d2bc07e28a8469ef0",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.23.0-7355174-py3-none-manylinux2014_x86_64.whl",
        )
        version(
            "1.23.0-cuda110",
            sha256="ede8245d3f7df181abdc5c5109a79be1ba9b6d888ca9f693f62db2c95efad267",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.23.0-7355173-py3-none-manylinux2014_x86_64.whl",
        )
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
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.22.0-6988993-py3-none-manylinux2014_x86_64.whl",
        )
    elif "linux" in system and arch == "aarch64":
        version(
            "1.27.0-cuda120",
            sha256="57700656c4dd411497d3f8c690d409c71d6a8e9c2cc5e70499098dd0a01fd56b",
            expand=False,
            preferred=True,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.27.0-8625314-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.27.0-cuda110",
            sha256="8c28429f979c3fcb45f40f08efdae4b6ed3f4743634d41722a6c94d18c4cd995",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.27.0-8625303-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.26.0-cuda120",
            sha256="9672969cab3d1a009b9e2bf3b139aec06af46f67a45a128098f8279736848079",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.26.0-8269288-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.26.0-cuda110",
            sha256="e90fcb896cc0ee22a0fa5476a8fde8227412683796367334636c3f844e208975",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.26.0-8269290-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.25.0-cuda120",
            sha256="f497ce8bf0df83e5c72b393a621d910bc712c6cdc4bbba6db50cf1cbc47d881b",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.25.0-7922358-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.25.0-cuda110",
            sha256="2eb94223ac980658606af6a56720ce963f4fd877c1291d08517f82ce435b4155",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.25.0-7922357-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.24.0-cuda120",
            sha256="2a7fab1d94b23edde1cee5b93918aca6b86417e3ffb4544adcb9961c73375014",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.24.0-7582307-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.24.0-cuda110",
            sha256="84711689dacc787dfd90bfc66da7ce4b1884a006b763109e9ecf0b07aefacbc2",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.24.0-7582302-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.23.0-cuda120",
            sha256="911d16b40c95b8cc700d3c96b40d3144953e7ffbb191ec22a75990c76cf638c3",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda120/nvidia_dali_cuda120-1.23.0-7355174-py3-none-manylinux2014_aarch64.whl",
        )
        version(
            "1.23.0-cuda110",
            sha256="ca58f2990825d18736c872f48d3f5e5dbda8de136ab6339f1f9f6984d7b3dffe",
            expand=False,
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.23.0-7355173-py3-none-manylinux2014_aarch64.whl",
        )
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
            url="https://developer.download.nvidia.com/compute/redist/nvidia-dali-cuda110/nvidia_dali_cuda110-1.22.0-6988993-py3-none-manylinux2014_aarch64.whl",
        )

    cuda120_versions = (
        "1.27.0-cuda120",
        "1.26.0-cuda120",
        "1.25.0-cuda120",
        "1.24.0-cuda120",
        "1.23.0-cuda120",
        "1.22.0-cuda120",
    )
    cuda110_versions = (
        "1.27.0-cuda110",
        "1.26.0-cuda110",
        "1.25.0-cuda110",
        "1.24.0-cuda110",
        "1.23.0-cuda110",
        "1.22.0-cuda110",
    )

    for v in cuda120_versions:
        depends_on("cuda@12", when=v, type=("build", "run"))
    for v in cuda110_versions:
        depends_on("cuda@11", when=v, type=("build", "run"))

    depends_on("python@3.6:3.11", when="@1.23:", type=("build", "run"))
    depends_on("python@3.6:3.10", when="@:1.22", type=("build", "run"))
    depends_on("py-astunparse@1.6.0:", type=("build", "run"))
    depends_on("py-gast@0.3.3:", when="@1.27:", type=("build", "run"))
    depends_on("py-gast@0.2.1:0.4.0", when="@:1.26", type=("build", "run"))
    depends_on("py-dm-tree", when="@1.27:", type=("build", "run"))
