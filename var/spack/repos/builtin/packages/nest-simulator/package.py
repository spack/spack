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


class NestSimulator(CMakePackage):
    """NEST is a simulator for spiking neural network models 

    It focuses on the dynamics, size and structure of neural systems rather
    than on the exact morphology of individual neurons."""

    homepage = "http://www.nest-simulator.org"
    url      = "https://github.com/nest/nest-simulator/releases/download/v2.12.0/nest-2.12.0.tar.gz"

    version('2.14.0', sha256='d6316d6c9153100a3220488abfa738958c4b65bf2622bd15540e4aa81e79f17f')
    version('2.12.0', sha256='bac578f38bb0621618ee9d5f2f1febfee60cddc000ff32e51a5f5470bb3df40d')
    version('2.10.0', sha256='2b6fc562cd6362e812d94bb742562a5a685fb1c7e08403765dbe123d59b0996c')
    version('2.8.0',  sha256='d47325b27a5599b6ea58a3c4ef06656e7c5a4941c4e94dec6a5c2fa956209915')
    version('2.6.0',  sha256='5fe4924bc57d0c7dd820aa371de935eedf7e813832c0eee2c976b33c9a8db4cf')
    version('2.4.2',  sha256='8f86e58c1a12b733ffabd8b0400326e5a3494a458149ea8ebe9f19674d05b91b')
    version('2.4.2_custom_tso',  sha256='8f86e58c1a12b733ffabd8b0400326e5a3494a458149ea8ebe9f19674d05b91b', url='https://github.com/nest/nest-simulator/releases/download/v2.4.2/nest-2.4.2.tar.gz')

    variant('python', default=True,
            description='Build the PyNest interface')
    variant('mpi', default=False,
            description='Build with MPI bindings')
    variant('optimize', default=True,
            description='Build with MPI bindings')
    variant('modules', default=False,
            description='Enables external module support')
    # TODO add variants for neurosim and music when these are in spack

    depends_on('python',            when='+python')
    depends_on('py-numpy',          when='+python')
    depends_on('py-cython@0.19.2:', when='+python')
    depends_on('py-nose',           when='+python')
    depends_on('py-setuptools',     when='+python')

    depends_on('mpi', when='+mpi')

    depends_on('doxygen')

    depends_on('gsl')
    depends_on('readline')
    depends_on('libtool')
    depends_on('pkg-config')

    extends('python', when='+python')

    patch('nest_2.4.2_tso.patch', when='@2.4.2_custom_tso',
          description='Fixes initial behavior of TSO models, looses O(10%)'
                      ' performance.')

    # Before 2.12.0 it was an autotools package
    @when('@:2.10.99')
    def cmake(self, spec, prefix):
        pass

    @when('@:2.10.99')
    def build(self, spec, prefix):
        pass

    @when('@:2.10.99')
    def install(self, spec, prefix):
        configure_args = ["CXXFLAGS=-std=c++03",
                          "--prefix=" + prefix,
                          "--with-openmp"]
        if '+python' in spec:
            configure_args.append("--with-python")
        else:
            configure_args.append("--without-python")
        if '+mpi' in spec:
            configure_args.append("--with-mpi")
        else:
            configure_args.append("--without-mpi")
        if '+optimize' in spec:
            configure_args.append("--with-optimize")
        else:
            configure_args.append("--without-optimize")

        configure(*configure_args)

        make()
        make("install")

    def cmake_args(self):
        args = []
        if '+mpi' in self.spec:
            args.append('-Dwith-mpi=ON')
        else:
            args.append('-Dwith-mpi=OFF')
        if '+python':
            args.append('-Dwith-python={0}'.format(self.spec['python'].version[0]))
        else:
            args.append('-Dwith-python=OFF')
        if '+optimize':
            args.append('-Dwith-optimize=ON')
        else:
            args.append('-Dwith-optimize=OFF')

        return args

    @when('+modules')
    @when('@:2.14.0')
    @run_after('install')
    def install_headers(self):
        # copy source files to installation folder for older versions
        # (these are needed for modules to build against)
        # see https://github.com/nest/nest-simulator/pull/844
        path_headers = join_path(prefix, "include", "nest")

        mkdirp(path_headers)

        for suffix in ["h", "hpp"]:
            for f in find_headers('*.{0}'.format(suffix),
                                  self.stage.source_path, recursive=True):
                install(f, path_headers)

    def setup_environment(self, spack_env, run_env):
        run_env.set("NEST_INSTALL_DIR", self.spec.prefix)
