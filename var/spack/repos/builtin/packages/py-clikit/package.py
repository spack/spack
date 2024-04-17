# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClikit(PythonPackage):
    """CliKit is a group of utilities to build beautiful and testable
    command line interfaces."""

    homepage = "https://github.com/sdispater/clikit"
    pypi = "clikit/clikit-0.6.2.tar.gz"

    license("MIT")

    version(
        "0.6.2",
        sha256="71268e074e68082306e23d7369a7b99f824a0ef926e55ba2665e911f7208489e",
        url="https://pypi.org/packages/f2/3d/4394c710b9195b83382dc67bdd1040e5ebfc3fc8df90e20fe74341298c57/clikit-0.6.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-crashtest@:0.3", when="@0.6: ^python@:3")
        depends_on("py-pastel@0.2:", when="@0.4.2:")
        depends_on("py-pylev@1.3:")
