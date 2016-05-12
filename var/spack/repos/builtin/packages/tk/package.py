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

class Tk(Package):
    """Tk is a graphical user interface toolkit that takes developing
       desktop applications to a higher level than conventional
       approaches. Tk is the standard GUI not only for Tcl, but for
       many other dynamic languages, and can produce rich, native
       applications that run unchanged across Windows, Mac OS X, Linux
       and more."""
    homepage = "http://www.tcl.tk"

    def url_for_version(self, version):
        return "http://prdownloads.sourceforge.net/tcl/tk%s-src.tar.gz" % version

    version('8.6.3', '85ca4dbf4dcc19777fd456f6ee5d0221')

    depends_on("tcl")

    def install(self, spec, prefix):
        with working_dir('unix'):
            configure("--prefix=%s" % prefix,
                      "--with-tcl=%s" % spec['tcl'].prefix.lib)
            make()
            make("install")
