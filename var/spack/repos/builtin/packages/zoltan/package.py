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
import re, os, glob
from spack import *

class Zoltan(Package):
    """The Zoltan library is a toolkit of parallel combinatorial algorithms for
       parallel, unstructured, and/or adaptive scientific applications.  Zoltan's
       largest component is a suite of dynamic load-balancing and paritioning
       algorithms that increase applications' parallel performance by reducing
       idle time.  Zoltan also has graph coloring and graph ordering algorithms,
       which are useful in task schedulers and parallel preconditioners."""

    homepage = "http://www.cs.sandia.gov/zoltan"
    base_url = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions"

    version('3.83', '1ff1bc93f91e12f2c533ddb01f2c095f')
    version('3.8', '9d8fba8a990896881b85351d4327c4a9')
    version('3.6', '9cce794f7241ecd8dbea36c3d7a880f9')
    version('3.3', '5eb8f00bda634b25ceefa0122bd18d65')

    variant('debug', default=False, description='Builds a debug version of the library')
    variant('shared', default=True, description='Builds a shared version of the library')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('mpi', default=False, description='Enable MPI support')

    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        config_args = [
            '--enable-f90interface' if '+fortan' in spec else '--disable-f90interface',
            '--enable-mpi' if '+mpi' in spec else '--disable-mpi',
        ]
        config_cflags = [
            '-O0' if '+debug' in spec else '-O3',
            '-g' if '+debug' in spec else '-g0',
        ]

        if '+shared' in spec:
            config_args.append('--with-ar=$(CXX) -shared $(LDFLAGS) -o')
            config_args.append('RANLIB=echo')
            config_cflags.append('-fPIC')

        if '+mpi' in spec:
            config_args.append('CC=%s/mpicc' % spec['mpi'].prefix.bin)
            config_args.append('CXX=%s/mpicxx' % spec['mpi'].prefix.bin)
            config_args.append('--with-mpi=%s' % spec['mpi'].prefix)
            config_args.append('--with-mpi-compilers=%s' % spec['mpi'].prefix.bin)

        # NOTE: Early versions of Zoltan come packaged with a few embedded
        # library packages (e.g. ParMETIS, Scotch), which messes with Spack's
        # ability to descend directly into the package's source directory.
        if spec.satisfies('@:3.6'):
            cd('Zoltan_v%s' % self.version)

        mkdirp('build')
        cd('build')

        config_zoltan = Executable('../configure')
        config_zoltan(
            '--prefix=%s' % pwd(),
            '--with-cflags=%s' % ' '.join(config_cflags),
            '--with-cxxflags=%s' % ' '.join(config_cflags),
            *config_args)

        make()
        make('install')

        # NOTE: Unfortunately, Zoltan doesn't provide any configuration options for
        # the extension of the output library files, so this script must change these
        # extensions as a post-processing step.
        if '+shared' in spec:
            for libpath in glob.glob('lib/*.a'):
                libdir, libname = (os.path.dirname(libpath), os.path.basename(libpath))
                move(libpath, os.path.join(libdir, re.sub(r'\.a$', '.so', libname)))

        mkdirp(prefix)
        move('include', prefix)
        move('lib', prefix)

    def url_for_version(self, version):
        return '%s/zoltan_distrib_v%s.tar.gz' % (Zoltan.base_url, version)
