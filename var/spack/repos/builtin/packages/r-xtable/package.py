# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXtable(RPackage):
    """Coerce data to LaTeX and HTML tables."""

    homepage = "http://xtable.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/xtable_1.8-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xtable"

    version('1.8-4', sha256='5abec0e8c27865ef0880f1d19c9f9ca7cc0fd24eadaa72bcd270c3fb4075fd1c')
    version('1.8-3', sha256='53b2b0fff8d7a8bba434063c2a01b867f510a4389ded2691fbedbc845f08c325')
    version('1.8-2', '239e4825cd046156a67efae3aac01d86')
