# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFpcompare(RPackage):
    """Reliable Comparison of Floating Point Numbers"""

    homepage = "https://github.com/PredictiveEcology/fpCompare"
    url      = "https://cloud.r-project.org/src/contrib/fpCompare_0.2.3.tar.gz"

    maintainers = ['dorton21']

    version('0.2.3', sha256='f89be3568544a3a44e4f01b5050ed03705805308ec1aa4add9a5e1b5b328dbdf')
