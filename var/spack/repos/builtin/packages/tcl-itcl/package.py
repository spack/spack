##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class TclItcl(AutotoolsPackage):
    """[incr Tcl] is the most widely used O-O system for Tcl. The name is a
    play on C++, and [incr Tcl] provides a similar object model, including
    multiple inheritence and public and private classes and variables."""

    homepage = "https://sourceforge.net/projects/incrtcl/"
    url      = "https://sourceforge.net/projects/incrtcl/files/%5Bincr%20Tcl_Tk%5D-4-source/itcl%204.0.4/itcl4.0.4.tar.gz"

    version('4.0.4', 'c9c52afdd9435490e2db17c3c6c95ab4')

    extends('tcl')

    def configure_args(self):
        args = [
            '--enable-shared',
            '--enable-threads',
            '--with-tcl=' + self.spec['tcl'].tcl_lib_dir,
        ]
        return args
