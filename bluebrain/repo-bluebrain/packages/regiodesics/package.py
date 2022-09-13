# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Regiodesics(CMakePackage):
    """Vector direction computation
    """

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BBPNSE/Computing+neurons+direction+vectors"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/archive/regiodesics.git"

    submodules = True

    version('0.1.2', tag='0.1.2')
    version('0.1.1', tag='0.1.1')
    version('0.1.0', tag='0.1.0')

    depends_on('boost@:1.70.0')
    depends_on('openscenegraph')
