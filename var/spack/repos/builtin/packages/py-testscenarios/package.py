# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestscenarios(PythonPackage):
    """Testscenarios, a pyunit extension for dependency injection"""

    homepage = "https://launchpad.net/testscenarios"
    pypi = "testscenarios/testscenarios-0.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.0",
        sha256="480263fa5d6e618125bdf092aab129a3aeed5996b1e668428f12cc56d6d01d28",
        url="https://pypi.org/packages/da/25/2f10da0d5427989fefa5ab51e697bc02625bbb7de2be3bc8452462efac78/testscenarios-0.5.0-py2.py3-none-any.whl",
    )
