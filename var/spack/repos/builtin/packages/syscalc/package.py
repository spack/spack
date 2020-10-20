# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Syscalc(MakefilePackage):
    """ A tool to derive theoretical systematic uncertainties"""

    homepage = "https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/SysCalc"
    url      = "http://madgraph.phys.ucl.ac.be/Downloads/SysCalc_V1.1.7.tar.gz"

    version('1.7', sha256='657272a158f459d1e983f2fee7cbb4b9c3931ecc793f3345fa8d7c3f515a4f34',
            url='http://madgraph.phys.ucl.ac.be/Downloads/SysCalc_V1.1.7.tar.gz')

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
