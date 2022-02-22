# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meshtool(MakefilePackage):
    """Meshtool - A mesh manipulation utility"""

    homepage = "https://bitbucket.org/aneic/meshtool/"
    git      = "https://bitbucket.org/aneic/meshtool.git"

    maintainers = ['MarieHouillon']

    version('master', branch='master')
    # Version to use with openCARP releases
    version('oc9.0', commit='6c5cfbd067120901f15a04bf63beec409bda6dc9')
    version('oc8.2', commit='6c5cfbd067120901f15a04bf63beec409bda6dc9')
    version('oc8.1', commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")
    version('oc7.0', commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('meshtool', prefix.bin)
