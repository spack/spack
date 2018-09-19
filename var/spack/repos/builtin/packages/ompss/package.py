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
import os
import glob


class Ompss(Package):
    """OmpSs is an effort to integrate features from the StarSs programming
       model developed by BSC into a single programming model. In
       particular, our objective is to extend OpenMP with new directives
       to support asynchronous parallelism and heterogeneity (devices
       like GPUs). However, it can also be understood as new directives
       extending other accelerator based APIs like CUDA or OpenCL. Our
       OmpSs environment is built on top of our Mercurium compiler and
       Nanos++ runtime system.

    """
    homepage = "http://pm.bsc.es/"
    url      = "http://pm.bsc.es/sites/default/files/ftp/ompss/releases/ompss-14.10.tar.gz"
    list_url = 'http://pm.bsc.es/ompss-downloads'

    version('14.10', '404d161265748f2f96bb35fd8c7e79ee')

    # all dependencies are optional, really
    depends_on("mpi")
    # depends_on("openmp")
    depends_on("hwloc")
    depends_on("extrae")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich' in spec:
            mpi = spec['mvapich']

        openmp_options = ["--enable-tl-openmp-profile"]
        if spec.satisfies('%intel'):
            openmp_options.append("--enable-tl-openmp-intel")

        os.chdir(glob.glob('./nanox-*').pop())
        configure("--prefix=%s" % prefix,
                  "--with-mcc=%s" % prefix,
                  "--with-extrae=%s" %
                  spec['extrae'].prefix,
                  "--with-hwloc=%s" % spec['hwloc'].prefix)
        make()
        make("install")

        os.chdir(glob.glob('../mcxx-*').pop())
        configure("--prefix=%s" % prefix,
                  "--with-nanox=%s" % prefix,
                  "--enable-ompss",
                  "--with-mpi=%s" % mpi.prefix,
                  *openmp_options)
        make()
        make("install")
