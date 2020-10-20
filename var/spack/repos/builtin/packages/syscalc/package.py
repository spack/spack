# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Syscalc(MakefilePackage):
    """ A tool to derive theoretical systematic uncertainties"""

    homepage = "https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/SysCalc"
    url      = "http://madgraph.phys.ucl.ac.be/Downloads/SysCalc_V1.1.7.tar.gz"

    version('1.1.7', sha256='d33219a525a54733bdfd02d8314288bdecd977fb1e97ddeaf13bf470bbbdd386')

    depends_on('lhapdf@6:')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        url += '/SysCalc_V{0}.tar.gz'

        url = url.format(version)
        return url

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('sys_calc', prefix.bin)
        install_tree('include', prefix.include)
