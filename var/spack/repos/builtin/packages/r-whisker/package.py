# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RWhisker(RPackage):
    """logicless templating, reuse templates in many programming languages
    including R"""

    homepage = "http://github.com/edwindj/whisker"
    url      = "https://cloud.r-project.org/src/contrib/whisker_0.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/whisker"

    version('0.3-2', 'c4b9bf9a22e69ce003fe68663ab5e8e6')
