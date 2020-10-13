# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClamd(PythonPackage):
    """clamd is a portable Python module to use the ClamAV anti-virus
    engine on Windows, Linux, MacOSX and other platforms. It requires
    a running instance of the clamd daemon."""

    homepage = "http://www.decalage.info/en/python/pyclamd"
    url      = "https://github.com/graingert/python-clamd/archive/1.0.2.tar.gz"

    version('1.0.2', sha256='baf5d8d3d9b182ebc21ed830bab6ac4e21ed43ee2bea8e1ed7672dbab834b880')
    version('1.0.1', sha256='44cd3364186fd8687e5b7208c59d603004f17b00cbf6329da07aa30b256a4ad1')
    version('1.0.0', sha256='72006b81d40f67c9858e671518cb4c76b76c687ec47a0809affabc323f6aa403')
    version('0.3.4', sha256='c35c4007ff8b1a57325940462c363d1ea2bd0b6a850e59912826deca056ee407')
    version('0.3.3', sha256='365d218952961e6647608147921ac43430a128844eac124e49ed909a4c59990a')

    depends_on('py-setuptools', type='build')
