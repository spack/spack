# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPkginfo(PythonPackage):
    """Query metadatdata from sdists / bdists / installed packages."""

    homepage = "https://code.launchpad.net/~tseaver/pkginfo/trunk"
    pypi = "pkginfo/pkginfo-1.5.0.1.tar.gz"

    license("MIT")

    version(
        "1.9.6",
        sha256="4b7a555a6d5a22169fcc9cf7bfd78d296b0361adad412a346c1226849af5e546",
        url="https://pypi.org/packages/b3/f2/6e95c86a23a30fa205ea6303a524b20cbae27fbee69216377e3d95266406/pkginfo-1.9.6-py3-none-any.whl",
    )
    version(
        "1.8.3",
        sha256="848865108ec99d4901b2f7e84058b6e7660aae8ae10164e015a6dcf5b242a594",
        url="https://pypi.org/packages/f3/28/ded592460bc65d39a48fe51d7678c408ae895ee3694d4cd404a131a73271/pkginfo-1.8.3-py2.py3-none-any.whl",
    )
    version(
        "1.7.1",
        sha256="37ecd857b47e5f55949c41ed061eb51a0bee97a87c969219d144c0e023982779",
        url="https://pypi.org/packages/77/83/1ef010f7c4563e218854809c0dff9548de65ebec930921dedf6ee5981f27/pkginfo-1.7.1-py2.py3-none-any.whl",
    )
    version(
        "1.5.0.1",
        sha256="a6d9e40ca61ad3ebd0b72fbadd4fba16e4c0e4df0428c041e01e06eb6ee71f32",
        url="https://pypi.org/packages/e6/d5/451b913307b478c49eb29084916639dc53a88489b993530fed0a66bab8b9/pkginfo-1.5.0.1-py2.py3-none-any.whl",
    )
