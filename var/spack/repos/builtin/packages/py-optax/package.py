# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOptax(PythonPackage):
    """A gradient processing and optimisation library in JAX."""

    homepage = "https://github.com/deepmind/optax"
    pypi = "optax/optax-0.1.7.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.1",
        sha256="fe1adcf2157ecfd83af05110b4ac0de142aa52baecc4e51c42490ac6d2867cd2",
        url="https://pypi.org/packages/dd/89/7e91e9ecf3bf1e4d0cdb7ffa3fc61e422968a9df0c38d66f6b564a8be336/optax-0.2.1-py3-none-any.whl",
    )
    version(
        "0.1.7",
        sha256="2b85115f2ae7adafe5fd9abf4b275e53057765361511c8ccc868e70158458494",
        url="https://pypi.org/packages/13/71/787cc24c4b606f3bb9f1d14957ebd7cb9e4234f6d59081721230b2032196/optax-0.1.7-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@0.1.9:")
        depends_on("python@3.8:", when="@0.1.5:0.1.8")
        depends_on("py-absl-py@0.7.1:")
        depends_on("py-chex@0.1.7:", when="@0.1.8:")
        depends_on("py-chex@0.1.5:", when="@0.1.4:0.1.7")
        depends_on("py-jax@0.1.55:")
        depends_on("py-jaxlib@0.1.37:")
        depends_on("py-numpy@1.18.0:")
