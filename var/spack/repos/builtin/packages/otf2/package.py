# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Otf2(AutotoolsPackage):
    """The Open Trace Format 2 is a highly scalable, memory efficient event
       trace data format plus support library.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "https://www.vi-hps.org/cms/upload/packages/otf2/otf2-2.1.1.tar.gz"

    version('2.2',   'd0519af93839dc778eddca2ce1447b1ee23002c41e60beac41ea7fe43117172d')
    version('2.1.1', 'e51ad0d8ca374d25f47426746ca629e7')
    version('2.1',   'e2994e53d9b7c2cbd0c4f564d638751e')
    version('2.0',   '5b546188b25bc1c4e285e06dddf75dfc')
    version('1.5.1', '16a9df46e0da78e374f5d12c8cdc1109')
    version('1.4',   'a23c42e936eb9209c4e08b61c3cf5092')
    version('1.3.1', 'd0ffc4e858455ace4f596f910e68c9f2')
    version('1.2.1', '8fb3e11fb7489896596ae2c7c83d7fc8')

    def configure_args(self):
        return [
            '--enable-shared',
            'CFLAGS={0}'.format(self.compiler.pic_flag),
            'CXXFLAGS={0}'.format(self.compiler.pic_flag)
        ]
