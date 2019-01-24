#------------------------------------------------------------------------------
# Copyright (c) 2017, University of Tennessee
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of Tennessee nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL UNIVERSITY OF TENNESSEE BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

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
