# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMinrpc(PythonPackage):
    """Minimalistic RPC utility (only used within cpymad and pytao)."""

    homepage = "https://github.com/hibtc/minrpc"
    pypi = "minrpc/minrpc-0.0.11.tar.gz"

    license("GPL-3.0-only")

    version(
        "0.0.11",
        sha256="f8f2d0398a63c052a0a303f009d26a8eca9b984be3210579a1dcd6819977c8cd",
        url="https://pypi.org/packages/bb/b0/96a29e109c65646fd87c126a2d9eaa2d37924ee8c793aa277d251fbba668/minrpc-0.0.11-py2.py3-none-any.whl",
    )
