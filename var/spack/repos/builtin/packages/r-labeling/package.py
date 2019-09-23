# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLabeling(RPackage):
    """Provides a range of axis labeling algorithms."""

    homepage = "https://cloud.r-project.org/package=labeling"
    url      = "https://cloud.r-project.org/src/contrib/labeling_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/labeling"

    version('0.3', 'ccd7082ec0b211aba8a89d85176bb534')
