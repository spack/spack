# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyEquinox(PythonPackage):
    """Equinox is a comprehensive JAX library that provides a wide
    range of tools and features not found in core JAX, including neural networks
    with PyTorch-like syntax, filtered APIs for transformations, PyTree manipulation
    routines, and advanced features like runtime errors."""

    homepage = "https://docs.kidger.site/equinox/"

    pypi = "equinox/equinox-0.11.10.tar.gz"

    maintainers("viperMl")

    license("Apache-2.0", checked_by="viperML")

    version("0.11.12", sha256="bee22aabaf7ee0cde6f2ae58cf3b981dea73d47e297361a0203e299208ef1739")
    version("0.11.10", sha256="f3e7d5545b71e427859a28050526d09adb6b20285c47476a606328a0b96c9509")

    depends_on("py-hatchling", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-jax@0.4.13:0.4.26", when="@:0.11.10")
        depends_on("py-jax@0.4.28:", when="@0.11.11:")
        depends_on("py-jaxtyping@0.2.20:")
        depends_on("py-typing-extensions@4.5.0:")
        depends_on("py-wadler-lindig@0.1.0:")
