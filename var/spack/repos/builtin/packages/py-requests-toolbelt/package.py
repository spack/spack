# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsToolbelt(PythonPackage):
    """A toolbelt of useful classes and functions to be used with
    python-requests"""

    homepage = "https://toolbelt.readthedocs.org/"
    pypi = "requests-toolbelt/requests-toolbelt-0.9.1.tar.gz"
    git = "https://github.com/requests/toolbelt.git"

    license("Apache-2.0")

    version(
        "1.0.0",
        sha256="cccfdd665f0a24fcf4726e690f65639d272bb0637b9b92dfd91a5568ccf6bd06",
        url="https://pypi.org/packages/3f/51/d4db610ef29373b879047326cbf6fa98b6c1969d6f6dc423279de2b1be2c/requests_toolbelt-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.1",
        sha256="380606e1d10dc85c3bd47bf5a6095f815ec007be7a8b69c878507068df059e6f",
        url="https://pypi.org/packages/60/ef/7681134338fc097acef8d9b2f8abe0458e4d87559c689a8c306d0957ece5/requests_toolbelt-0.9.1-py2.py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="42c9c170abc2cacb78b8ab23ac957945c7716249206f90874651971a4acff237",
        url="https://pypi.org/packages/97/8a/d710f792d6f6ecc089c5e55b66e66c3f2f35516a1ede5a8f54c13350ffb0/requests_toolbelt-0.8.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests@2.0.1:", when="@0.6.1:")
