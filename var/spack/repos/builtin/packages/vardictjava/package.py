# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Vardictjava(Package):
    """VarDictJava is a variant discovery program written in Java.
    It is a partial Java port of VarDict variant caller."""

    homepage = "https://github.com/AstraZeneca-NGS/VarDictJava"
    url      = "https://github.com/AstraZeneca-NGS/VarDictJava/releases/download/v1.5.1/VarDict-1.5.1.tar"

    version('1.5.1', '8c0387bcc1f7dc696b04e926c48b27e6')
    version('1.4.4', '6b2d7e1e5502b875760fc9938a0fe5e0')

    depends_on('java@8:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bin/VarDict', prefix.bin)

        mkdirp(prefix.lib)
        files = [x for x in glob.glob("lib/*jar")]
        for f in files:
            install(f, prefix.lib)
