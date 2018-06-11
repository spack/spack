##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class LmSensors(MakefilePackage):
    """The lm-sensors package provides user-space support for the
    hardware monitoring drivers in Linux."""

    homepage = "https://github.com/groeck/lm-sensors/"
    url      = "https://github.com/groeck/lm-sensors/archive/V3-4-0.tar.gz"

    version('3-4-0', '1e9f117cbfa11be1955adc96df71eadb')
    version('3-3-5', '42dcbc32c61133f5dbcdfd7ef8d0ee3c')
    version('3-3-4', 'b2bee2bc0b2dedc92b8ef60b719b87a3')
    version('3-3-3', 'e9be751b91c619cef3fd1ccfc22d0ded')
    version('3-3-2', 'd580e0cf872768c2670ab0721b1dedc9')
    version('3-3-1', 'e03c761365dd89ebc04913166018281b')
    version('3-3-0', '97f22cb084420aee88f765df084b8cd0')
    version('3-2-0', '07cd13fecb0e0ea19ddf97ec797ee222')
    version('3-1-2', '4031e02c566992e6a6fd87af018c457e')
    version('3-1-1', '2a62fb3789972756ff2ad2d3ad3f016c')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix),
             'ETCDIR={0}/etc'.format(prefix))
