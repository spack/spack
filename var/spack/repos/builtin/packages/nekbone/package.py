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
import os


class Nekbone(Package):
    """NEK5000 emulation software called NEKbone. Nekbone captures the basic
       structure and user interface of the ex- tensive Nek5000 software.
       Nek5000 is a high order, incompressible Navier-Stokes solver based on
       the spectral element method."""

    homepage = "https://github.com/ANL-CESAR/"
    url = "https://github.com/ANL-CESAR/nekbone.git"

    tags = ['proxy-app']

    version('master', git='https://github.com/ANL-CESAR/nekbone.git')

    def install(self, spec, prefix):

        if not os.path.exists(prefix.bin):
            mkdir(prefix.bin)

        os.chdir(os.getcwd() + '/test/example1/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/example1/'):
            mkdir(prefix.bin + '/example1/')

        install('nekbone', prefix.bin + '/example1/')
        install('nekpmpi', prefix.bin + '/example1/')

        os.chdir('../example2/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/example2/'):
            mkdir(prefix.bin + '/example2/')

        install('nekbone', prefix.bin + '/example2/')
        install('nekpmpi', prefix.bin + '/example2/')

        os.chdir('../example3/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/example3/'):
            mkdir(prefix.bin + '/example3/')

        install('nekbone', prefix.bin + '/example3/')
        install('nekpmpi', prefix.bin + '/example3/')

        os.chdir('../nek_comm/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/nek_comm/'):
            mkdir(prefix.bin + '/nek_comm/')
        install('nekbone', prefix.bin + '/nek_comm/')
        install('nekpmpi', prefix.bin + '/nek_comm/')

        os.chdir('../nek_delay/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/nek_delay/'):
            mkdir(prefix.bin + '/nek_delay/')
        install('nekbone', prefix.bin + '/nek_delay/')
        install('nekpmpi', prefix.bin + '/nek_delay/')

        os.chdir('../nek_mgrid/')
        os.system('./makenek ex1  ../../src')

        if not os.path.exists(prefix.bin + '/nek_mgrid/'):
            mkdir(prefix.bin + '/nek_mgrid/')

        install('nekbone', prefix.bin + '/nek_mgrid/')
        install('nekpmpi', prefix.bin + '/nek_mgrid/')

