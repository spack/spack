# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GftlShared(CMakePackage):
    """
    Provides common gFTL containers of Fortran intrinsic types that
    are encountered frequently.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared"
    git = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared.git"

    maintainers = ['kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    version('1.5.0', commit='6b60a685e59dc30d3a25ad0b5a1d0de9dc610b76', submodules=True)
    version('1.4.1', commit='1c85cb233d195f3fb5eb51ceb362c3bf09f2d7c4', submodules=True)
    version('1.3.6', commit='b4a11c3ae3f0a5d43f25c83ae9b508975fc48e6f', submodules=True)
    version('1.3.5', commit='221940d8852e0f2b6366fa6bfc1f45ae1e9751f1', submodules=True)
    version('1.3.3', commit='0351c67ab6f37c4815f0829aa1ca826c3d78e769', submodules=True)
    version('1.3.0', commit='8f770ee380a99c72dbc525cff0699924be052848', submodules=True)

    depends_on('m4', type=('build', 'run'))
    depends_on('git', type=('build'))
