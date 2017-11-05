##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install example
#
# You can edit this file again by typing:
#
#     spack edit example
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from subprocess import call

class Nek5000(Package):
    """A fast and scalable high-order solver for computational fluid
       dynamics"""

    homepage = "https://nek5000.mcs.anl.gov/"
    url      = "https://github.com/Nek5000/Nek5000"

    tags = ['cfd', 'flow', 'hpc', 'solver', 'navier-stokes', \
                                         'spectral-elements', 'fluid']

    version('17.0.0-beta2', git = 'https://github.com/Nek5000/Nek5000.git', \
               commit = 'b95f46c59f017fff2fc19b66aa65a881085a7572')
    version('develop', git = 'https://github.com/Nek5000/Nek5000.git', \
           branch='master')

    variant('mpi', default=True, description='Build with MPI.')

    depends_on('mpi', when="+mpi", type=('build'))

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.fc:
            msg = 'Cannot build Nek5000 without a Fortran compiler.'
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        toolsDir   = 'tools'
        binDir     = 'bin'
        installDir = prefix.bin

        F77 = spack_f77
        CC  = spack_cc

        mkdirp(installDir)

        # Build the tools, no need to install, maketools does this
        # be default
        with working_dir(toolsDir):
            filter_file(r'^F77\s*=.*', 'F77=\"' + F77 + '\"',  'maketools')
            filter_file(r'^CC\s*=.*' , 'CC=\"'  + CC  + '\"',  'maketools')
            makeTools = Executable('./maketools')
            makeTools('all')

        with working_dir(binDir):
            if '+mpi' in spec:
                F77 = spec['mpi'].mpif77
                CC  = spec['mpi'].mpicc

            filter_file(r'^F77\s*=.*', 'F77=\"' + F77 + '\"',  'makenek')
            filter_file(r'^CC\s*=.*' , 'CC=\"'  + CC  + '\"',  'makenek')
            filter_file(r'SOURCE_ROOT\s*=\"\$H.*',  'SOURCE_ROOT=\"'  + \
                                             prefix.bin.Nek5000 + '\"',  'makenek')

            install('makenek', installDir)
            install('genbox' , installDir)
            call('cp -r ../../Nek5000 '  + installDir, shell=True)
