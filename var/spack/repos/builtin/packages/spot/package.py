# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spot(AutotoolsPackage):
    """Spot is a C++11 library for omega-automata manipulation and model
       checking."""
    homepage = "https://spot.lrde.epita.fr/"
    url      = "http://www.lrde.epita.fr/dload/spot/spot-1.99.3.tar.gz"

    version('1.99.3', 'd53adcb2d0fe7c69f45d4e595a58254e')
    version('1.2.6', '799bf59ccdee646d12e00f0fe6c23902')

    variant('python', default=True, description='Enable python API')

    depends_on("python@3.3:", when='@1.99.5: +python')
    depends_on("python@3.2:", when='@1.99: +python')
    depends_on("python@2:", when='+python')
    depends_on('boost', when='@:1.2.6')
