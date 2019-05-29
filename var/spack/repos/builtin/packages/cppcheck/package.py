# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cppcheck(MakefilePackage):
    """A tool for static C/C++ code analysis."""
    homepage = "http://cppcheck.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/cppcheck/cppcheck/1.78/cppcheck-1.78.tar.bz2"

    version('1.87', sha256='e3b0a46747822471df275417d4b74b56ecac88367433e7428f39288a32c581ca')
    version('1.81', '0c60a1d00652044ef511bdd017689938')
    version('1.78', 'f02d0ee0a4e71023703c6c5efff6cf9d')
    version('1.72', '2bd36f91ae0191ef5273bb7f6dc0d72e')
    version('1.68', 'c015195f5d61a542f350269030150708')

    variant('htmlreport', default=False, description="Install cppcheck-htmlreport")

    depends_on('py-pygments', when='+htmlreport', type='run')

    def build(self, spec, prefix):
        make('CFGDIR={0}'.format(prefix.cfg))

    def install(self, spec, prefix):
        # Manually install the final cppcheck binary
        mkdirp(prefix.bin)
        install('cppcheck', prefix.bin)
        install_tree('cfg', prefix.cfg)
        if spec.satisfies('+htmlreport'):
            install('htmlreport/cppcheck-htmlreport', prefix.bin)
