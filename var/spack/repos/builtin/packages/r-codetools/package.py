# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCodetools(RPackage):
    """Code analysis tools for R."""

    homepage = "https://cloud.r-project.org/package=codetools"
    url      = "https://cloud.r-project.org/src/contrib/codetools_0.2-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/codetools"

    version('0.2-16', sha256='f67a66175cb5d8882457d1e9b91ea2f16813d554fa74f80c1fd6e17cf1877501')
    version('0.2-15', '37419cbc3de81984cf6d9b207d4f62d4')
    version('0.2-14', '7ec41d4f8bd6ba85facc8c5e6adc1f4d')

    depends_on('r@2.1:', type=('build', 'run'))
