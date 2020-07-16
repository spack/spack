# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Syscalc(MakefilePackage):
    """ A tool to derive theoretical systematic uncertainties"""

    homepage = "https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/SysCalc"
    url      = "http://madgraph.phys.ucl.ac.be/Downloads/SysCalc_V1.1.6.tar.gz"

    version('1.1.7', sha256='1b563771c972acfefcfc2dd9fed452a508b560ffdec826c427c8f5fb6eb2d76b')
    version('1.1.6', sha256='c4cc82a5582ba0517c832b2c0f78ca264c07e0dc68a0256de9f38426c67b1786')

    depends_on('lhapdf@6:')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        url += '/SysCalc_V{0}.tar.gz'
        
        url = url.format(version)
        return url

    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        mkdirp(prefix.bin)
        install('sys_calc', prefix.bin)
        install_dir('include')
