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


class Jchronoss(CMakePackage):
    """ JCHRONOSS aims to help HPC application testing process
     to scale as much as the application does. """

    homepage = "http://jchronoss.hpcframework.com"
    url      = "http://fs.paratools.com/mpc/contrib/apps/jchronoss/JCHRONOSS-1.2.tar.gz"

    version('1.2',   'f083ca453537e4f60ad17d266bbab1f1')
    version('1.1.1', '2d78a0998efec20e7726af19fff76a72')
    version('1.1',   'a8ba0b21b18548874b8ab2a6ca6e1081')
    version('1.0',   '78d81e00248e21f4adea4a1ccfd6156b')

    variant("realtime", default=False, description="Enable Real-Time support")
    variant("openmp", default=False, description="Enable OpenMP constructs")
    variant("ncurses", default=False, description="Enable ncurses-based tool")
    variant('color', default=False, description='Enable colour-themed output')

    depends_on("libxml2")
    depends_on("libwebsockets", when="+realtime")
    depends_on("libev", when="+realtime")
    depends_on("ncurses", when="+ncurses")

    def cmake_args(self):
        args = ["-DSPACK_DRIVEN=ON"]

        if '+color' in self.spec:
            args.append("-DENABLE_COLOR=yes")
        if '+openmp' in self.spec:
            args.append("-DENABLE_OPENMP=yes")
        if '+ncurses' in self.spec:
            args.append("-DENABLE_PLUGIN_NCURSES=yes")
        if '+realtime' in self.spec:
            args.append("-DENABLE_PLUGIN_SERVER=yes")

        return args
