# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyroApi(PythonPackage):
    """Generic API for dispatch to Pyro backends."""

    homepage = "https://github.com/pyro-ppl/pyro-api"
    pypi = "pyro-api/pyro-api-0.1.2.tar.gz"

    version(
        "0.1.2",
        sha256="10e0e42e9e4401ce464dab79c870e50dfb4f413d326fa777f3582928ef9caf8f",
        url="https://pypi.org/packages/fc/81/957ae78e6398460a7230b0eb9b8f1cb954c5e913e868e48d89324c68cec7/pyro_api-0.1.2-py3-none-any.whl",
    )
