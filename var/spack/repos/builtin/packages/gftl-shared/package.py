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
    url = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/releases/download/v1.4.1/gFTL-shared-1.4.1.tar"

    maintainers = ['kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    depends_on('m4', type=('build', 'run'))

    version('1.4.1', 
        sha256='78a1c20fe75430df0e2abc5d324905cf52ad22346080b66925bca514d90ff94a',
        url='https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/releases/download/v1.4.1/gFTL-shared-1.4.1.tar')

    version('1.3.6', 
        sha256='6a6d618581b0d15213b2700b15102921f557340b73c7710405525641824e8703',
        url='https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/releases/download/v1.3.6/gFTL-shared-v1.3.6.tar')
    
    version('1.3.0', 
        sha256='c9e8090fb74900bbfd6cc9a0f75626180062be18d8671d48bb46dd087880e6b2',
        url='https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/releases/download/v1.3.0/gFTL-shared-v1.3.0.tar')
