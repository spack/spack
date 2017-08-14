##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
from spack import *
import tarfile
import glob
from distutils.dir_util import copy_tree


class Mcb(MakefilePackage):
    """The "Monte Carlo Benchmark" (MCB) is intended for use in exploring
    the computational performance of Monte Carlo algorithms on parallel
    architectures.
    """

    tags = ['proxy-app']
    homepage = "https://codesign.llnl.gov/mcb.php"
    url = "https://codesign.llnl.gov/downloads/mcb-20130723.tar.gz"

    version('20130723', 'ed9c97edb45c8918184b4eba280bd884')
    depends_on('mpi')
    depends_on('boost')


    parallel = False
    
    build_directory = 'src'
    @property
    def build_targets(self):
        targets = []
        targets.append('BOOST_INCLUDE = -I{0} '.format(self.spec['boost'].prefix.include.boost))
        targets.append('BOOST_LIB = -L{0} -Wl,-rpath {0}'.format(self.spec['boost'].prefix.lib))
        targets.append('CXX = %s' % self.spec['mpi'].mpicc)
        targets.append('OPENMPFLAG = %s' % self.compiler.openmp_flag)
        targets.append('MPI_INCLUDE = -I%s' % self.spec['mpi'].prefix.include)
        targets.append('CXXFLAGS = -O2 -xHost $(CXXDEFINES) $(OPENMPFLAG)')
        return targets
        
###
#    def edit(self, spec, prefix):
#        for fname in glob.glob('*.*'):
#            if (fname.endswith("tgz")):
#                tar = tarfile.open(fname, "r:gz")
#                tar.extractall()
#                tar.close()
#        with working_dir('src'):
#            filter_file(r'^BOOST_INCLUDE\s*=.*',
#                        'BOOST_INCLUDE = -I{0} '.format(self.spec['boost'].prefix.include.boost),
#                        'Makefile')
#            filter_file(r'^BOOST_LIB\s*=.*',
#                        'BOOST_LIB = -L{0} -Wl,-rpath {0}'.format(self.spec['boost'].prefix.lib),
#                        'Makefile')
#            filter_file(r'^CXX\s*=.*', 'CXX = %s' % self.spec['mpi'].mpicc,
#                        'Makefile')
#            filter_file(r'^OPENMPFLAG\s*=.*',
#                        'OPENMPFLAG = %s' % self.compiler.openmp_flag,
#                        'Makefile')
#            filter_file(r'^MPI_INCLUDE\s*=.*',
#                        'MPI_INCLUDE = -I%s' % self.spec['mpi'].prefix.include,
#                        'Makefile')
#            filter_file(r'^CXXFLAGS\s*=.*',
#                        'CXXFLAGS = -O2 -xHost $(CXXDEFINES) $(OPENMPFLAG)',
#                        'Makefile')
###

    def install(self, spec, prefix):
        install_tree('src/Documentation', prefix.doc)
        mkdirp(prefix.doc.install)
        install('README', prefix.doc.install)
        install('src/README', prefix.doc)