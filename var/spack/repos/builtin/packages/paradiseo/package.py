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
import sys

class Paradiseo(Package):
    """A C++ white-box object-oriented framework dedicated to the reusable design of metaheuristics."""
    homepage = "http://paradiseo.gforge.inria.fr/"

    # Installing from the development version is a better option at this 
    # point than using the very old supplied packages
    version('head', git='https://gforge.inria.fr/git/paradiseo/paradiseo.git')
    # This is a version that the package formula author has tested successfully.
    # However, the clone is very large (~1Gb git history). The history in the 
    # head version has been trimmed significantly.
    version('dev-safe', git='https://gforge.inria.fr/git/paradiseo/paradiseo.git',
             commit='dbb8fbe9a786efd4d1c26408ac1883442e7643a6')

    variant('mpi',      default=True,  description='Compile with parallel and distributed metaheuristics module')
    variant('smp',      default=True,  description='Compile with symmetric multi-processing module ')
    variant('edo',      default=True,  description='Compile with (Experimental) EDO module')
    #variant('tests',    default=False, description='Compile with build tests')
    #variant('doc',      default=False, description='Compile with documentation')
    variant('debug',    default=False, description='Builds a debug version of the libraries')
    variant('openmp',   default=False, description='Enable OpenMP support')
    variant('gnuplot',  default=False, description='Enable GnuPlot support')
    
    # Required dependencies
    depends_on ("cmake")

    # Optional dependencies
    depends_on ("mpi", when="+mpi")
    depends_on ("doxygen", when='+doc')
    depends_on ("gnuplot", when='+gnuplot')
    depends_on ("eigen", when='+edo')
    depends_on ("boost~mpi", when='+edo~mpi')
    depends_on ("boost+mpi", when='+edo+mpi')

    # Patches
    patch('enable_eoserial.patch')
    patch('fix_osx_detection.patch')
    patch('fix_tests.patch')
    patch('fix_tutorials.patch')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        options.extend([
            '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
            '-DINSTALL_TYPE:STRING=MIN',
            '-DMPI:BOOL=%s' % ('TRUE' if '+mpi' in spec else 'FALSE'),
            '-DSMP:BOOL=%s' % ('TRUE' if '+smp' in spec else 'FALSE'), # Note: This requires a C++11 compatible compiler
            '-DEDO:BOOL=%s' % ('TRUE' if '+edo' in spec else 'FALSE'),
            '-DENABLE_CMAKE_TESTING:BOOL=%s' % ('TRUE' if '+tests' in spec else 'FALSE'),
            '-DENABLE_OPENMP:BOOL=%s' % ('TRUE' if '+openmp' in spec else 'FALSE'),
            '-DENABLE_GNUPLOT:BOOL=%s' % ('TRUE' if '+gnuplot' in spec else 'FALSE')
        ])
 
        with working_dir('spack-build', create=True):
            # Configure
            cmake('..', *options)

            # Build, test and install
            make("VERBOSE=1")
            if '+tests' in spec:
                make("test")
            make("install")
