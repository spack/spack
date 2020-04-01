# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exampm(CMakePackage):
    """Exascale Material Point Method (MPM) Mini-App"""

    homepage = "https://github.com/ECP-copa/ExaMPM"
    git      = "https://github.com/ECP-copa/ExaMPM.git"

    version('develop', branch='master')

    tags = ['proxy-app']
