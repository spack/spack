# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchGeometric(PythonPackage):
    """Graph Neural Network Library for PyTorch."""

    homepage = "https://pyg.org/"
    pypi = "torch-geometric/torch_geometric-2.5.3.tar.gz"
    git = "https://github.com/pyg-team/pytorch_geometric.git"

    license("MIT")
    maintainers("adamjstewart")

    version("2.5.3", sha256="ad0761650c8fa56cdc46ee61c564fd4995f07f079965fe732b3a76d109fd3edc")
    version(
        "2.1.0.post1",
        sha256="32347402076ccf60fa50312825178f1e3e5ce5e7b3b3a8b2729ac699da24525d",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="347f693bebcc8a621eda4867dafab91c04db5f596d7ed7ecb89b242f8ab5c6a1",
        deprecated=True,
    )
    version(
        "1.6.0",
        sha256="fbf43fe15421c9affc4fb361ba4db55cb9d3c64d0c29576bb58d332bf6d27fef",
        deprecated=True,
    )

    depends_on("py-flit-core@3.2:3", when="@2.4:", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-tqdm")
        depends_on("py-numpy")
        depends_on("py-scipy")
        depends_on("py-fsspec", when="@2.5:")
        depends_on("py-jinja2")
        depends_on("py-aiohttp", when="@2.5:")
        depends_on("py-requests")
        depends_on("py-pyparsing", when="@1.7.2:")
        depends_on("py-scikit-learn")
        depends_on("py-psutil@5.8:", when="@2.2:")

        # Undocumented dependencies
        depends_on("py-torch")

    # Historical dependencies
    depends_on("py-setuptools", type="build", when="@:2.3")
    with when("@:1"):
        depends_on("py-pytest-runner", type="build")
        depends_on("py-networkx", type=("build", "run"))
        depends_on("py-python-louvain", type=("build", "run"), when="@1.6.2:")
        depends_on("py-numba", type=("build", "run"))
        depends_on("py-pandas", type=("build", "run"))
        depends_on("py-rdflib", type=("build", "run"))
        depends_on("py-googledrivedownloader", type=("build", "run"))
        depends_on("py-h5py~mpi", type=("build", "run"))
        depends_on("py-ase", type=("build", "run"))
