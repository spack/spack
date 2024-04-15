# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJraph(PythonPackage):
    """Jraph: A library for Graph Neural Networks in Jax."""

    homepage = "https://github.com/deepmind/jraph"
    pypi = "jraph/jraph-0.0.6.dev0.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.6.dev0",
        sha256="350fe37bf717f934f1f84fd3370a480b3178bfcb61dfa217c738971308c57625",
        url="https://pypi.org/packages/2a/e2/f799edeb39a154560b52134cdb3a3359e2de965c76886949966e46d5c42b/jraph-0.0.6.dev0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-jax@0.1.55:")
        depends_on("py-jaxlib@0.1.37:")
        depends_on("py-numpy@1.18.0:")
