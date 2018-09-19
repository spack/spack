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


class TclTcllib(AutotoolsPackage):
    """Tcllib is a collection of utility modules for Tcl. These modules provide
    a wide variety of functionality, from implementations of standard data
    structures to implementations of common networking protocols. The intent is
    to collect commonly used function into a single library, which users can
    rely on to be available and stable."""

    homepage   = "http://www.tcl.tk/software/tcllib"
    url        = "https://sourceforge.net/projects/tcllib/files/tcllib/1.19/tcllib-1.19.tar.gz"
    list_url   = "https://sourceforge.net/projects/tcllib/files/tcllib/"
    list_depth = 1

    version('1.19', '8d3990d01e3fb66480d441d18a7a7d0d')
    version('1.18', '219361e6bdf9d9c0d79edbd1ab3e8080')
    version('1.17', '4c75fbfbb518f8990fcd4686b976bd70')
    version('1.16', 'e65e91f5ca188648019fdbe15fbfb9bf')
    version('1.15', '7a0525912e8863f8d4360ab10e5450f8')
    version('1.14', '55bac9afce54c3328f368918cc2d7a4b')

    extends('tcl')
