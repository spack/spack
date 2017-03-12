##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import sys


class Wx(AutotoolsPackage):
    """wxWidgets is a C++ library that lets developers create
       applications for Windows, Mac OS X, Linux and other platforms
       with a single code base. It has popular language bindings for
       Python, Perl, Ruby and many other languages, and unlike other
       cross-platform toolkits, wxWidgets gives applications a truly
       native look and feel because it uses the platform's native API
       rather than emulating the GUI. It's also extensive, free,
       open-source and mature."""
    homepage = "http://www.wxwidgets.org/"
    url      = "https://github.com/wxWidgets/wxWidgets/releases/download/v3.1.0/wxWidgets-3.1.0.tar.bz2"

    version('3.1.0', '2170839cfa9d9322e8ee8368b21a15a2497b4f11')
    version('3.0.2', '6461eab4428c0a8b9e41781b8787510484dea800')
    version('3.0.1', '73e58521d6871c9f4d1e7974c6e3a81629fddcf8')

    version('develop', git='https://github.com/wxWidgets/wxWidgets.git', branch='master')

    depends_on('gtkplus')

    @when('@:3.0.2')
    def build(self, spec, prefix):
        make(parallel=False)

    def configure_args(self):
        spec = self.spec
        options = [
            '--enable-unicode',
            '--disable-precomp-headers'
        ]

        # see http://trac.wxwidgets.org/ticket/17639
        if spec.satisfies('@:3.1.0') and sys.platform == 'darwin':
            options.extend([
                '--disable-qtkit',
                '--disable-mediactrl'
            ])

        return options
