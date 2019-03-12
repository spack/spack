# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Draco(CMakePackage):
    """Draco is an object-oriented component library geared towards numerically
    intensive, radiation (particle) transport applications built for parallel
    computing hardware. It consists of semi-independent packages and a robust
    build system. """

    homepage = "https://github.com/lanl/draco"
    url = "https://github.com/lanl/Draco/archive/draco-7_1_0.zip"
    git = "https://github.com/lanl/Draco.git"

    version('develop', branch='develop')
    version('7_1_0',  sha256='eca6bb86eb930837fb5e09b76c85c200b2c1522267cc66f81f2ec11a8262b5c9')
    version('6_25_0', sha256='e27eba44f397e7d111ff9a45b518b186940f75facfc6f318d76bd0e72f987440')
    version('6_23_0', sha256='edf20308746c06647087cb4e6ae7656fd057a89091a22bcba8f17a52e28b7849')
    version('6_22_0', sha256='4d1ed54944450c4ec7d00d7ba371469506c6985922f48f780bae2580c9335b86')
    version('6_21_0', sha256='f1ac88041606cdb1dfddd3bc74db0f1e15d8fc9d0a1eed939c8aa0fa63a85b55')
    version('6_20_1', sha256='b1c51000c9557e0818014713fce70d681869c50ed9c4548dcfb2e9219c354ebe')
    version('6_20_0', sha256='a6e3142c1c90b09c4ff8057bfee974369b815122b01d1f7b57888dcb9b1128f6')

    variant('lapack', default=False, description='Enable LAPACK Wrapper')
    variant('eospac', default=False, description='Enable EOSPAC Support')

    depends_on('mpi@3:')
    depends_on('random123')
    depends_on('gsl')
    depends_on('python')
    depends_on('lapack', when='+lapack')
    depends_on('eospac', when='+eospac')
