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


class Motif(AutotoolsPackage):
    """"
    Motif - Graphical user interface (GUI)
    specification and the widget toolkit
    """
    homepage = "http://motif.ics.com/"
    url = "http://cfhcable.dl.sourceforge.net/project/motif/Motif 2.3.8 Source Code/motif-2.3.8.tar.gz"

    version('2.3.8', '7572140bb52ba21ec2f0c85b2605e2b1')

    depends_on("flex")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("libxft")
    depends_on("libxcomposite")
    depends_on("libxfixes")
    depends_on("xbitmaps")
