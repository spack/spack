##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class Cppcheck(MakefilePackage):
    """A tool for static C/C++ code analysis."""
    homepage = "http://cppcheck.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/cppcheck/cppcheck/1.78/cppcheck-1.78.tar.bz2"

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
