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
#
# Author: Samuel Knight <sknigh@sandia.gov>
# Date: Feb 3, 2017
#
from spack import *


class SstMacro(AutotoolsPackage):
    """The SST/macro software package provides a simulator for large-scale
    parallel computer architectures for the coarse-grained study of
    distributed-memory applications. The simulator is driven from either a
    trace file or skeleton application. SST/macro's modular architecture can
    be extended with additional network models, trace file formats,
    software services, and processor models.
    """

    homepage = "http://sst.sandia.gov/about_sstmacro.html"
    url      = "https://github.com/sstsimulator/sst-macro/releases/download/v6.1.0_Final/sstmacro-6.1.0.tar.gz"
    git      = "https://github.com/sstsimulator/sst-macro.git"

    version('master', branch='master')
    version('6.1.0', '98b737be6326b8bd711de832ccd94d14')

    depends_on('boost@1.59:')
    depends_on('autoconf@1.68:', type='build', when='@master')
    depends_on('automake@1.11.1:', type='build', when='@master')
    depends_on('libtool@1.2.4:', type='build', when='@master')
    depends_on('m4', type='build', when='@master')

    @run_before('autoreconf')
    def bootstrap(self):
        if '@master' in self.spec:
            Executable('./bootstrap.sh')()

    def configure_args(self):
        args = ['--disable-regex']
        return args
