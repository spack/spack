# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFracdiff(RPackage):
    """Maximum likelihood estimation of the parameters of a
    fractionally differenced ARIMA(p,d,q) model (Haslett and
    Raftery, Appl.Statistics, 1989)."""

    homepage = "https://cloud.r-project.org/package=fracdiff"
    url      = "https://cloud.r-project.org/src/contrib/fracdiff_1.4-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fracdiff"

    version('1.4-2', '6a6977d175ad963d9675736a8f8d41f7')
