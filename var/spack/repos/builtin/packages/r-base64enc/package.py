# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBase64enc(RPackage):
    """This package provides tools for handling base64 encoding. It is more
    flexible than the orphaned base64 package."""

    homepage = "http://www.rforge.net/base64enc"
    url      = "https://cloud.r-project.org/src/contrib/base64enc_0.1-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/base64enc"

    version('0.1-3', '0f476dacdd11a3e0ad56d13f5bc2f190')

    depends_on('r@2.9.0:', type=('build', 'run'))
