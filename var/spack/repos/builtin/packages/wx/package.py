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

class Wx(Package):
    """wxWidgets is a C++ library that lets developers create
       applications for Windows, Mac OS X, Linux and other platforms
       with a single code base. It has popular language bindings for
       Python, Perl, Ruby and many other languages, and unlike other
       cross-platform toolkits, wxWidgets gives applications a truly
       native look and feel because it uses the platform's native API
       rather than emulating the GUI. It's also extensive, free,
       open-source and mature."""
    homepage = "http://www.wxwidgets.org/"

    version('2.8.12', '2fa39da14bc06ea86fe902579fedc5b1',
            url="https://sourceforge.net/projects/wxwindows/files/2.8.12/wxWidgets-2.8.12.tar.gz")
    version('3.0.1', 'dad1f1cd9d4c370cbc22700dc492da31',
            url="https://sourceforge.net/projects/wxwindows/files/3.0.1/wxWidgets-3.0.1.tar.bz2")

    depends_on('gtkplus')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--enable-unicode", "--disable-precomp-headers")

        make(parallel=False)
        make("install")

