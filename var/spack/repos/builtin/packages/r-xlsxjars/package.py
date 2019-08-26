# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXlsxjars(RPackage):
    """The xlsxjars package collects all the external jars required for the
    xlxs package. This release corresponds to POI 3.10.1."""

    homepage = "https://cloud.r-project.org/package=xlsxjars"
    url      = "https://cloud.r-project.org/src/contrib/xlsxjars_0.6.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xlsxjars"

    version('0.6.1', '5a1721d5733cb42f3a29e3f353e39166')

    depends_on('r-rjava', type=('build', 'run'))
