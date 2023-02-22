# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatasets(PythonPackage):
    """Datasets is a lightweight library providing two main
    features: one-line dataloaders for many public datasets and
    efficient data pre-processing."""

    homepage = "https://github.com/huggingface/datasets"
    pypi = "datasets/datasets-1.8.0.tar.gz"

    maintainers("thomas-bouvier")

    version("2.8.0", sha256="a843b69593914071f921fc1086fde939f30a63415a34cdda5db3c0acdd58aff2")
    version("1.8.0", sha256="d57c32bb29e453ee7f3eb0bbca3660ab4dd2d0e4648efcfa987432624cab29d3")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-pyarrow@1:3+parquet", type=("build", "run"), when="@:1.8.0")
    depends_on("py-pyarrow@6:+parquet", type=("build", "run"), when="@2.8.0:")
    depends_on("py-dill@:0.3.6", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-requests@2.19:", type=("build", "run"))
    depends_on("py-tqdm@4.27:4.49", type=("build", "run"), when="@:1.8.0")
    depends_on("py-tqdm@4.62.1:", type=("build", "run"), when="@2.8.0:")
    depends_on("py-xxhash", type=("build", "run"))
    depends_on("py-multiprocess", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
    depends_on("py-huggingface-hub@:0.0", type=("build", "run"), when="@:1.8.0")
    depends_on("py-huggingface-hub@0.2:0", type=("build", "run"), when="@2.8.0:")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-aiohttp", type=("build", "run"), when="@2.8.0:")
    depends_on("py-responses@:0.18", type=("build", "run"), when="@2.8.0:")
    depends_on("py-pyyaml@5.1:", type=("build", "run"), when="@2.8.0:")

    with when("@:1.8.0"):
        depends_on("py-fsspec", type=("build", "run"), when="^python@3.8:")
        depends_on("py-fsspec@:0.8.0", type=("build", "run"), when="^python@:3.7")
    depends_on("py-fsspec@2021.11.1:+http", type=("build", "run"), when="@2.8.0:")
