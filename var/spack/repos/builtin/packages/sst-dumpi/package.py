# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Samuel Knight <sknigh@sandia.gov>
# Date: Feb 3, 2017
#
from spack import *


class SstDumpi(AutotoolsPackage):
    """The DUMPI package provides libraries to collect and read traces of MPI
    applications. Traces are created by linking an application with a library
    that uses the PMPI interface to intercept MPI calls. DUMPI records
    signatures of all MPI-1 and MPI-2 subroutine calls, return values, request
    information, and PAPI counters.
    """

    homepage = "http://sst.sandia.gov/about_dumpi.html"
    url      = "https://github.com/sstsimulator/sst-dumpi/archive/6.1.0.tar.gz"
    git      = "https://github.com/sstsimulator/sst-dumpi.git"

    version('master', branch='master')
    version('6.1.0', '31c3f40a697dc85bf23dd34270982319')

    depends_on('autoconf@1.68:', type='build')
    depends_on('automake@1.11.1:', type='build')
    depends_on('libtool@1.2.4:', type='build')
    depends_on('m4', type='build')
