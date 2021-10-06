# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Garfieldpp(CMakePackage):
    """Garfield++ is a toolkit for the detailed simulation of particle
       detectors based on ionisation measurement in gases and semiconductors. """

    homepage = "https://garfieldpp.web.cern.ch/garfieldpp/"
    url      = "https://gitlab.cern.ch/garfield/garfieldpp/-/archive/4.0/garfieldpp-4.0.tar.gz"
    git      = "https://gitlab.cern.ch/garfield/garfieldpp.git"

    tags = ['hep']

    maintainers = ['mirguest']

    version('master', branch='master')
    version('4.0', sha256='82bc1f0395213bd30a7cd854426e6757d0b4155e99ffd4405355c9648fa5ada3')
    version('3.0', sha256='c1282427a784658bc38b71c8e8cfc8c9f5202b185f0854d85f7c9c5a747c5406')

    depends_on('root')
