##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class IsaacServer(CMakePackage):
    """In Situ Animation of Accelerated Computations: Server"""

    homepage = "http://computationalradiationphysics.github.io/isaac/"
    url      = "https://github.com/ComputationalRadiationPhysics/isaac/archive/v1.3.0.tar.gz"
    git      = "https://github.com/ComputationalRadiationPhysics/isaac.git"

    maintainers = ['ax3l']

    version('develop', branch='dev')
    version('master', branch='master')
    version('1.4.0', '3ad05c8fad4673366077204c5d39285f')
    version('1.3.3', '7aeebaf0c5a77e2cb9bea066750e369b')
    version('1.3.2', 'c557daa74de52fd79e734c9758fca38b')
    version('1.3.1', '7fe075f9af68d05355eaba0e224f20ca')
    version('1.3.0', 'c8a794da9bb998ef0e75449bfece1a12')

    # variant('gstreamer', default=False, description= \
    #         'Support for RTP streams, e.g. to Twitch or Youtube')

    depends_on('cmake@3.3:', type='build')
    depends_on('jpeg', type='link')
    depends_on('jansson', type='link')
    depends_on('boost@1.56.0:', type='link')
    depends_on('libwebsockets@2.1.1:', type='link')
    # depends_on('gstreamer@1.0', when='+gstreamer')

    # https://github.com/ComputationalRadiationPhysics/isaac/pull/70
    patch('jpeg.patch', when='@:1.3.1')

    root_cmakelists_dir = 'server'
