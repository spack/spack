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


class Wxpropgrid(Package):
    """wxPropertyGrid is a property sheet control for wxWidgets. In
       other words, it is a specialized two-column grid for editing
       properties such as strings, numbers, flagsets, string arrays,
       and colours."""
    homepage = "http://wxpropgrid.sourceforge.net/"
    url      = "http://prdownloads.sourceforge.net/wxpropgrid/wxpropgrid-1.4.15-src.tar.gz"

    version('1.4.15', 'f44b5cd6fd60718bacfabbf7994f1e93')

    depends_on("wx")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--with-wxdir=%s" %
                  spec['wx'].prefix.bin, "--enable-unicode")

        make()
        make("install")
