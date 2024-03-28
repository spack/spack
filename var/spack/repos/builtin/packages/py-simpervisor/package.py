# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimpervisor(PythonPackage):
    """
    simpervisor provides the SupervisedProcess class that provides async methods
    start, ready, terminate, and kill to manage it.
    """

    homepage = "https://github.com/jupyterhub/simpervisor"
    pypi = "simpervisor/simpervisor-0.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4",
        sha256="8af72599d089efcfff30a86266de44b874b689611baa1345213795624fbd74fa",
        url="https://pypi.org/packages/91/bb/61db1f8e008a4dcd668e8be37bd29a2f3dbd615f503686649c82fc3e544b/simpervisor-0.4-py3-none-any.whl",
    )
