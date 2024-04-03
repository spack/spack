# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExtras(PythonPackage):
    """Useful extra bits for Python - things that shold be in the standard
    library."""

    homepage = "https://github.com/testing-cabal/extras"
    pypi = "extras/extras-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="f689f08df47e2decf76aa6208c081306e7bd472630eb1ec8a875c67de2366e87",
        url="https://pypi.org/packages/03/e9/e915af1f97914cd0bc021e125fd1bfd4106de614a275e4b6866dd9a209ac/extras-1.0.0-py2.py3-none-any.whl",
    )
