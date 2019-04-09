# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LmSensors(MakefilePackage):
    """The lm-sensors package provides user-space support for the
    hardware monitoring drivers in Linux. """

    homepage = "https://github.com/groeck/lm-sensors/"
    url = "https://github.com/groeck/lm-sensors/archive/V3-4-0.tar.gz"
    maintainers = ['G-Ragghianti']

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

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('perl', type='run')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix),
             'ETCDIR={0}/etc'.format(prefix))
