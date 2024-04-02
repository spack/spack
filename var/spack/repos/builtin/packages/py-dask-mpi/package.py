# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskMpi(PythonPackage):
    """Deploying Dask using MPI4Py."""

    homepage = "https://github.com/dask/dask-mpi"
    pypi = "dask-mpi/dask-mpi-2.21.0.tar.gz"

    skip_modules = ["dask_mpi.tests"]

    license("BSD-3-Clause")

    version(
        "2022.4.0",
        sha256="fa3a76512291ce22923c83085cc3d9b115aaa5a325a607d505754d3d7c5879b2",
        url="https://pypi.org/packages/25/a5/195604b42f504aa9b133d28114ad8a3fd503acd1c36acaff2dd3b1d9568b/dask_mpi-2022.4.0-py3-none-any.whl",
    )
    version(
        "2.21.0",
        sha256="80d787952eb4117c2072515d0991fbe82277920d0cef2c1c3f5039290626275a",
        url="https://pypi.org/packages/84/d6/e0338667a37cff9d665df4803a3f9c31f5d938dd79f4093cb6e07141744d/dask_mpi-2.21.0-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="89d776eec1886d424eb62aaa979e54551891a96420e180a74dd35be0ff021579",
        url="https://pypi.org/packages/f2/09/777bfd5484bdcf29839608c10d98124d9c1ded74fe63200218888182c7cb/dask_mpi-2.0.0-py3-none-any.whl",
    )

    # jupyter-server-proxy is not a needed dependency; https://github.com/dask/dask-mpi/pull/102
    # this significantly reduces the dependency tree of py-dask-mpi
