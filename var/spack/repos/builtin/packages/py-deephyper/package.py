# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDeephyper(PythonPackage):
    """Scalable asynchronous neural architecture and hyperparameter
    search for deep neural networks."""

    homepage = "https://deephyper.readthedocs.io/"
    pypi = "deephyper/deephyper-0.4.2.tar.gz"
    git = "https://github.com/deephyper/deephyper.git"

    maintainers("mdorier", "Deathn0t")

    license("BSD-3-Clause")

    version("0.9.3", sha256="e28f9f6ca596edee7fa73f7377ca17ddab99ac4b3c7f15db27cb6e786f770f23")
    version("0.8.1", sha256="ac27edd62ff81fcfb9b0b49f44963dadd8338be687f8f616d4cbdd6f5c68e511")

    # Variants for machine learning features
    variant("jax-cpu", default=False, description="Build with JAX dependencies")
    variant("torch", default=False, description="Build with PyTorch dependencies")

    # Variants for storage/parallel backends
    variant("mpi", default=False, description="Build with MPI dependencies")
    variant("ray", default=False, description="Build with Ray dependencies")
    variant("redis", default=False, description="Build with Redis dependencies")

    # Variants for developers
    variant("dev", default=False, description="Build with dev dependencies")

    with default_args(deprecated=True):
        version("master", branch="master")
        version("0.6.0", sha256="cda2dd7c74bdca4203d9cd637c4f441595f77bae6d77ef8e4a056b005357de34")
        version("0.4.2", sha256="ee1811a22b08eff3c9098f63fbbb37f7c8703e2f878f2bdf2ec35a978512867f")

    with default_args(type="build"):
        depends_on("py-hatchling@1.25:", when="@0.9:")

        depends_on("py-setuptools@42:", when="@0.6.0")
        depends_on("py-setuptools@40:49.1", when="@:0.6")

        depends_on("py-wheel@0.36.2", when="@:0.6")

        depends_on("py-cython@0.29.24:", when="@0.6.0")
        depends_on("py-cython@0.29.24:2", when="@0.4.2")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.9:")
        depends_on("python@3.9:", when="@0.8:")
        depends_on("python@3.7:3.11", when="@0.6.0")
        depends_on("python@3.7:3.9", when="@0.4.2")

        depends_on("py-configspace@1.1.1:", when="@0.8:")
        depends_on("py-configspace@0.4.20:")

        depends_on("py-cloudpickle", when="@0.9.3:")

        depends_on("py-dm-tree")

        depends_on("py-jinja2@3.1.4:", when="@0.8:")
        depends_on("py-jinja2@:3.1", when="@0.6.0")
        depends_on("py-jinja2@:3.0", when="@0.4.2")

        depends_on("py-loky@3.4:")

        depends_on("py-matplotlib")

        depends_on("py-numpy@1.26:", when="@0.8:")
        depends_on("py-numpy@1.20:", when="@0.6.0")
        depends_on("py-numpy")

        depends_on("py-pandas@0.24.2:")

        depends_on("py-packaging@20.5:", when="@0.6.0 target=aarch64: platform=darwin")
        depends_on("py-packaging")

        depends_on("py-parse", when="@0.8:")

        depends_on("py-scikit-learn@0.23.1:")

        depends_on("py-scipy@1.10:", when="@0.8:")
        depends_on("py-scipy@1.7:", when="@0.6.0")
        depends_on("py-scipy@0.19.1:")

        depends_on("py-tqdm@4.64.0:")

        depends_on("py-psutil", when="@0.8:")

        # https://github.com/spack/spack/pull/49603
        # depends_on("py-pymoo@0.6:", when="@0.8:")

        depends_on("py-pyyaml")

        depends_on("py-tinydb", when="@0.4.2")

        depends_on("py-alive-progress@3.2.0:", when="@0.8:")

        depends_on("openssl@3.4.0:", when="@0.8:")

        with when("+dev"):
            depends_on("py-pytest")

            with when("@0.9.3:"):
                depends_on("py-pytest")
                depends_on("py-tox")
                depends_on("py-twine")
                depends_on("py-ruff")
                # depends_on("py-rstcheck")
                depends_on("py-gitpython")
                depends_on("py-ipython")
                depends_on("py-nbsphinx")
                depends_on("py-sphinx@5:")
                # depends_on("py-sphinx-book-theme@1.1.3")
                # depends_on("py-pydata-sphinx-theme@0.15.4")
                depends_on("py-sphinx-copybutton")
                depends_on("py-sphinx-design@0.6.1")
                depends_on("py-sphinx-gallery")
                # depends_on("py-sphinx-lfs-content")
                # depends_on("py-sphinx-togglebutton")

        # Jax for GPU is not currently available on Spack
        with when("+jax-cpu"):
            depends_on("py-jax@0.3.25:", when="@0.8.1:")
            # depends_on("py-numpyro@0.15.3:", when="@0.8:")

        with when("+torch"):
            depends_on("py-torch@2:", when="@0.8.1:")

        with when("+mpi"):
            depends_on("py-mpi4py@3.1.3:", when="@0.8.1:")

        with when("+ray"):
            depends_on("py-ray@1.3.0:", when="@0.8.1:")

        with when("+redis"):
            depends_on("py-redis")
            # depends_on("redisjson")
