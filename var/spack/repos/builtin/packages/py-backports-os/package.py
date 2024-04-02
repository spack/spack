# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsOs(PythonPackage):
    """Backport of new features in Python's os module"""

    homepage = "https://github.com/pjdelport/backports.os"
    pypi = "backports.os/backports.os-0.1.1.tar.gz"

    license("PSF-2.0")

    version(
        "0.1.1",
        sha256="05b2801a021753d33e3402ac8857a3ba395eb7febbd7381fb27d880d07803061",
        url="https://pypi.org/packages/2b/e0/e7f8afefb8219e6b686722923db073b5bd54e1336b5a8b32da66c2edd0e8/backports.os-0.1.1-py3-none-any.whl",
    )
