# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBase64(RPackage):
    """Compatibility wrapper to replace the orphaned package by Romain
       Francois. New applications should use the 'openssl' or 'base64enc'
       package instead."""

    homepage = "https://cloud.r-project.org/package=base64"
    url      = "https://cloud.r-project.org/src/contrib/base64_2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/base64"

    version('2.0', 'f5a653842f75ad717ef6a00969868ae5')

    depends_on('r-openssl', type=('build', 'run'))
