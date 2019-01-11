# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpileaks(Package):
    """Tool to detect and report MPI objects like MPI_Requests and
    MPI_Datatypes."""

    homepage = "https://github.com/hpc/mpileaks"
    url      = "https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

    version('1.0', '8838c574b39202a57d7c2d68692718aa')

    variant('stackstart', values=int, default=0, description='Specify the number of stack frames to truncate.')

    depends_on('mpi')
    depends_on('adept-utils')
    depends_on('callpath')

    def install(self, spec, prefix):
        stackstart = int(self.spec.variants['stackstart'].value)
        confargs = ['--with-adept-utils=%s' % self.spec['adept-utils'].prefix,
                    '--with-callpath=%s' % self.spec['callpath'].prefix,
                    '--prefix=%s' % self.spec.prefix]
        if stackstart:
            confargs.extend(['--with-stack-start-c=%s' % stackstart,
                             '--with-stack-start-fortran=%s' % stackstart])
        configure(*confargs)
        make()
        make('install')
