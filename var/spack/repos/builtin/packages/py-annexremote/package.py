# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnnexremote(PythonPackage):
    """git annex special remotes made easy."""

    homepage = "https://github.com/Lykos153/AnnexRemote"
    pypi = "annexremote/annexremote-1.5.0.tar.gz"

    license("GPL-3.0-only")

    version(
        "1.6.0",
        sha256="bc5bd2e456d64679e33d71226705673ac213040f8ae495467e9629b550c2ca53",
        url="https://pypi.org/packages/66/81/32d0563cd017cca305a8b8883abb177880cedde1385213a6b4b33cc07e45/annexremote-1.6.0-py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="5aa99e37036c84547cc1f39eb3f99bf4079f1e5de1272b147e8dd32c0e14884f",
        url="https://pypi.org/packages/cd/9c/ced3458fcd0bb048350b7048412f6fa732ca7c44f6389d68c15e96e8b216/annexremote-1.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-future", when="@1.3:1.5")
