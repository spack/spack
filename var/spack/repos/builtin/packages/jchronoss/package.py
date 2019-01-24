# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
