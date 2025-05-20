# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDeephyper(PythonPackage):
    """Scalable asynchronous hyperparameter optimization, neural architecture search,
    and parallel ensemble of predictive models."""

    homepage = "https://deephyper.readthedocs.io/"
    pypi = "deephyper/deephyper-0.9.3.tar.gz"
    git = "https://github.com/deephyper/deephyper.git"

    maintainers("mdorier", "Deathn0t", "bretteiffert")

    tags = ["e4s"]

    license("BSD-3-Clause")

    # Versions
    version("master", branch="master")
    version("develop", branch="develop")
    version("0.9.3", sha256="e28f9f6ca596edee7fa73f7377ca17ddab99ac4b3c7f15db27cb6e786f770f23")
    version("0.8.1", sha256="ac27edd62ff81fcfb9b0b49f44963dadd8338be687f8f616d4cbdd6f5c68e511")

    # Variants for machine learning features
    # exists upstream, disabled in Spack due to missing dependencies, contributions welcome
    # variant("jax-cpu", default=False, description="Build with JAX dependencies")
    variant("torch", default=False, description="Build with PyTorch dependencies")

    # Variants for storage/parallel backends
    variant("mpi", default=False, description="Build with MPI dependencies")
    variant("ray", default=False, description="Build with Ray dependencies")
    # exists upstream, disabled in Spack due to missing dependencies, contributions welcome
    # variant("redis", default=False, description="Build with Redis dependencies")

    # Variants for developers
    variant("dev", default=False, description="Build with dev dependencies")

    with default_args(deprecated=True):
        version("0.6.0", sha256="cda2dd7c74bdca4203d9cd637c4f441595f77bae6d77ef8e4a056b005357de34")
        version("0.4.2", sha256="ee1811a22b08eff3c9098f63fbbb37f7c8703e2f878f2bdf2ec35a978512867f")

    # Build backend
    with default_args(type="build"):
        depends_on("py-hatchling@1.25:", when="@master")
        depends_on("py-hatchling@1.25:", when="@develop")
        depends_on("py-hatchling@1.25:", when="@0.9:")

        depends_on("py-setuptools@42:", when="@0.8:")
        depends_on("py-setuptools@42:", when="@0.6.0")
        depends_on("py-setuptools@40:49.1", when="@:0.6")

        depends_on("py-cython@0.29.24:", when="@0.8:")
        depends_on("py-cython@0.29.24:", when="@0.6.0")
        depends_on("py-cython@0.29.24:2", when="@0.4.2")

        depends_on("py-wheel@0.36.2", when="@:0.6")

    # Python versions
    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.9:")
        depends_on("python@3.9:", when="@0.8:")
        depends_on("python@3.7:3.11", when="@0.6.0")
        depends_on("python@3.7:3.9", when="@0.4.2")

    # Dependencies from setup/toml files
    with default_args(type=("build", "run")):
        depends_on("py-alive-progress@3.2.0:", when="@0.8:")
        depends_on("py-configspace@1.1.1:", when="@0.8:")
        depends_on("py-configspace@0.4.20:")
        depends_on("py-cloudpickle", when="@0.9.3:")
        depends_on("py-dm-tree")
        depends_on("py-jinja2@3.1.4:", when="@0.8:")
        depends_on("py-jinja2@:3.1", when="@0.6.0")
        depends_on("py-jinja2@:3.0", when="@0.4.2")
        depends_on("py-loky@3.4:", when="@0.9.3:")
        depends_on("py-matplotlib")
        depends_on("py-numpy@1.26.0:", when="@0.8:")
        depends_on("py-numpy@1.20:", when="@0.6.0")
        depends_on("py-numpy")
        depends_on("openssl@3.4.0:", when="@0.8:")
        depends_on("py-pandas@0.24.2:")
        depends_on("py-packaging@20.5:", when="@0.6.0 target=aarch64: platform=darwin")
        depends_on("py-packaging")
        depends_on("py-parse", when="@0.8:")
        depends_on("py-psutil", when="@0.8:")
        depends_on("py-pymoo@0.6:", when="@0.8:")
        depends_on("py-pyyaml", when="@0.8:")
        depends_on("py-scikit-learn@0.23.1:")
        depends_on("py-scipy@1.10:", when="@0.8:")
        depends_on("py-scipy@1.7:", when="@0.6.0")
        depends_on("py-scipy@0.19.1:")
        depends_on("py-tqdm@4.64.0:")
        depends_on("py-psutil", when="@0.8:")
        depends_on("py-pymoo@0.6:", when="@0.8:")
        depends_on("py-pyyaml")
        depends_on("py-tinydb", when="@0.4.2")

    with when("+dev"), default_args(type=("build", "run")):
        depends_on("py-pytest")

    # # Jax for GPU is not currently available on Spack
    # with when("+jax-cpu"), default_args(type=("build", "run")):
    #     depends_on("py-jax@0.4.3:", when="@0.8:")
    #     depends_on("py-numpyro@0.15.3:", when="@0.8:")

    with when("+torch"), default_args(type=("build", "run")):
        depends_on("py-torch@2:", when="@0.8:")

    with when("+mpi"), default_args(type=("build", "run")):
        depends_on("py-mpi4py@3:", when="@0.8:")

    with when("+ray"), default_args(type=("build", "run")):
        depends_on("py-ray", when="@0.8:")

    # with when("+redis"), default_args(type=("build", "run")):
    #     depends_on("py-redis")
    #     depends_on("redisjson")
