# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyOptax(PythonPackage):
    """A gradient processing and optimisation library in JAX."""

    homepage = "https://github.com/deepmind/optax"
    pypi = "optax/optax-0.1.7.tar.gz"

    license("Apache-2.0")

    version("0.2.4", sha256="4e05d3d5307e6dde4c319187ae36e6cd3a0c035d4ed25e9e992449a304f47336")
    version("0.2.1", sha256="fc9f430fa057377140d00aa50611dabbd7e8f4999e3c7543f641f9db6997cb1a")
    version("0.1.7", sha256="6a5a848bc5e55e619b187c749fdddc4a5443ea14be85cc769f995779865c110d")

    depends_on("python@3.9:", when="@0.2.1:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.1.7", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-absl-py@0.7.1:", type=("build", "run"))
    depends_on("py-chex@0.1.7:", when="@0.2.1:", type=("build", "run"))
    depends_on("py-chex@0.1.5:", when="@0.1.7", type=("build", "run"))
    depends_on("py-chex@0.1.89:", when="@0.2.4", type=("build", "run"))
    depends_on("py-jax@0.1.55:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.37:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", type=("build", "run"))
    depends_on("py-etils@1.7.0", type=("build", "run"), when="@0.2.3:0.2.4")
