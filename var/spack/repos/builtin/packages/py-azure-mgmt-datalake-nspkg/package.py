# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAzureMgmtDatalakeNspkg(PythonPackage):
    # BEGIN VERSIONS [WHEEL ONLY]
    version(
        "3.0.1",
        sha256="2ac6fa13c55b87112199c5fb03a3098cefebed5f44ac34ab3d39b399951b22c4",
        url="https://pypi.org/packages/48/3d/c65a520d93448923a96784582a0deafaae096cb37b444ae5d63b57f0562d/azure_mgmt_datalake_nspkg-3.0.1-py3-none-any.whl",
    )
    # END VERSIONS

    # BEGIN VARIANTS
    # END VARIANTS
    # BEGIN DEPENDENCIES
    with default_args(type=("build", "run")):
        depends_on("py-azure-mgmt-nspkg@3:", when="@3:")
    # END DEPENDENCIES
