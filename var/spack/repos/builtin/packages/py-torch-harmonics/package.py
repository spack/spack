# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchHarmonics(PythonPackage):
    """A differentiable spherical harmonic transform for PyTorch."""

    homepage = "https://github.com/NVIDIA/torch-harmonics"
    pypi = "torch_harmonics/torch_harmonics-0.6.5.tar.gz"

    maintainers("adamjstewart")

    license("BSD")

    version(
        "0.6.5",
        sha256="9751af83d7b6a3ff0f6d9887a30e0dcfb303ee956ce65e9e777128e4677cc17e",
        url="https://pypi.org/packages/51/40/83a1949410a546460a8baa6af9cadf8891cff7d36fe27e1d60d0d0008846/torch_harmonics-0.6.5-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-numpy")
        depends_on("py-torch")
        depends_on("py-triton", when="@0.6.4:")
