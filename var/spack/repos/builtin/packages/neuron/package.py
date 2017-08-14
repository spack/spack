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
import os
import sys
from spack import *


class Neuron(Package):

    """NEURON is a simulation environment for modeling individual
    and networks of neurons. NEURON models individual neurons via
    the use of sections that are automatically subdivided into individual
    compartments, instead of requiring the user to manually create
    compartments. The primary scripting language is hoc but a Python
    interface is also available."""

    homepage = "https://www.neuron.yale.edu/"
    url      = "http://www.neuron.yale.edu/ftp/neuron/versions/v7.4/nrn-7.4.tar.gz"
    github   = "https://github.com/nrnhines/nrn"

    version('7.4', '2c0bbee8a9e55d60fa26336f4ab7acbf')
    version('7.3', '993e539cb8bf102ca52e9fefd644ab61')
    version('7.2', '5486709b6366add932e3a6d141c4f7ad')
    version('develop', git=github, preferred=True)

    variant('mpi',           default=True,  description='Enable MPI parallelism')
    variant('python',        default=True,  description='Enable python')
    variant('static',        default=True,  description='Build static libraries')
    variant('cross-compile', default=False, description='Build for cross-compile environment')
    variant('multisend',     default=True, description="Enable multi-send spike exchange")

    depends_on('automake',   type='build')
    depends_on('autoconf',   type='build')
    depends_on('libtool',    type='build')
    depends_on('pkg-config', type='build')
    depends_on('python@2.6:', when='+python')
    depends_on('mpi', when='+mpi')

    # on bg-q mpi needs to be enabled : todo test this
    conflicts('~mpi', when='platform=bgq')

    # pgi compiler can't build static libraries
    conflicts('%pgi', when='+static')

    def url_for_version(self, version):
        url = "http://www.neuron.yale.edu/ftp/neuron/versions/v{0}/nrn-{0}.tar.gz"
        return url.format(version, version)

    def patch(self):
        # neuron use aclocal which need complete include path especially on os x
        pkgconfig_inc = '-I %s/share/aclocal/' % (self.spec['pkg-config'].prefix)
        libtool_inc = '-I %s/share/aclocal/' % (self.spec['libtool'].prefix)
        newpath = 'aclocal -I m4 %s %s' % (pkgconfig_inc, libtool_inc)
        filter_file(r'aclocal -I m4', r'%s' % newpath, "build.sh")

    def get_arch_options(self, spec):
        options = []

        if 'bgq' in self.spec.architecture:
            options.extend(['--enable-bluegeneQ',
                            '--host=powerpc64',
                            '--without-memacs'])

        if 'cray' in self.spec.architecture:
            options.extend(['--without-memacs',
                            '--without-nmodl',
                            'cross_compiling=yes'])

            # TODO: on cray systems we get an error while linking even if
            # we use cc wrapper. Hence add explicitly add mpi library
            if spec.satisfies('+mpi'):
                options.append('LIBS=-lmpich')

            # TODO: -pthread is not a valid pthread option for cray compiler.
            # for now disable use of pthread with cray compiler.
            if spec.satisfies('%cce'):
                options.append('use_pthread=no')

        return options

    def get_opt_flags(self):
        if 'bgq' in self.spec.architecture:
            return '-O3 -qtune=qp -qarch=qp -q64 -qstrict -qnohot -g'
        else:
            return '-O2 -g'

    def get_arch_dir(self):
        if 'bgq' in self.spec.architecture:
            arch = 'powerpc64'
        elif 'cray' in self.spec.architecture:
            arch = 'x86_64'
        else:
            arch = self.spec.architecture.target

        return arch

    def get_python_options(self, spec):
        options = []

        if spec.satisfies('+python'):
            py_prefix = spec['python'].prefix
            py_version = 'python{0}'.format(spec['python'].version.up_to(2))
            python_exec = '%s/bin/%s' % (py_prefix, py_version)

            options.append('--with-nrnpython=%s' % python_exec)
            options.append('--disable-pysetup')

            if spec.satisfies('+cross-compile'):
                # on cross compile builds we have to provide
                # PYINCDIR, PYLIB, PYLIBDIR etc

                py_lib = spec['python'].prefix.lib
                py_inc = '%s/include/%s' % (py_prefix, py_version)

                if not os.path.isdir(py_lib):
                    py_lib = spec['python'].prefix.lib64

                options.extend(['PYINCDIR=%s' % (py_inc),
                                'PYLIB=-L%s -l%s' % (py_lib, py_version),
                                'PYLIBDIR=%s' % py_lib,
                                'PYLIBLINK=-L%s -l%s' % (py_lib, py_version)])
        else:
            options.append('--without-nrnpython')
        return options

    def get_compiler_options(self, spec):
        options = []
        flags = self.get_opt_flags()

        # TODO: issue with static build and pgi compiler.
        # need to add fpic and enabled-shared
        if spec.satisfies('%pgi'):
            options.extend(['CFLAGS=-fPIC %s' % flags,
                            'CXXFLAGS=-fPIC %s' % flags,
                            '--enable-shared'])
        else:
            options.extend(['CFLAGS=%s' % flags,
                            'CXXFLAGS=%s' % flags])

        return options

    def get_configure_options(self, spec):
        options = []

        if spec.satisfies('+static'):
            options.extend(['--disable-shared',
                            'linux_nrnmech=no'])

        # on os-x disable building carbon 'click' utility (deprecated)
        if(sys.platform == 'darwin'):
            options.extend(['macdarwin=no'])

        options.extend(self.get_arch_options(spec))
        options.extend(self.get_python_options(spec))
        options.extend(self.get_compiler_options(spec))
        return options

    def build_nmodl(self, spec, prefix):
        # TODO: NEURON has two stage compilation for systems
        # like cray and bg-q. On these platforms it's ok to
        # use gcc and g++ as front-end compilers.
        options = ['--prefix=%s' % prefix,
                   '--with-nmodl-only',
                   '--without-x',
                   'CC=%s' % which("gcc"),
                   'CXX=%s' % which("g++")]

        configure = Executable(join_path(self.stage.source_path, 'configure'))
        configure(*options)
        make()
        make('install')

    def install(self, spec, prefix):
        c_compiler = spack_cc
        cxx_compiler = spack_cxx

        # for bg-q we can't set XL as CC and CXX compiler
        if 'bgq' in self.spec.architecture:
            c_compiler = spec['mpi'].mpicc
            cxx_compiler = spec['mpi'].mpicxx

        options = ['--prefix=%s' % prefix,
                   '--without-iv',
                   '--without-x',
                   '--without-readline',
                   '--disable-rx3d',
                   'CC=%s' % c_compiler,
                   'CXX=%s' % cxx_compiler]

        if spec.satisfies('+multisend'):
            options.append('--with-multisend')

        if spec.satisfies('+mpi'):
            options.extend(['MPICC=%s' % spec['mpi'].mpicc,
                            'MPICXX=%s' % spec['mpi'].mpicxx,
                            '--with-paranrn'])
        else:
            options.append('--without-paranrn')

        options.extend(self.get_configure_options(spec))
        build = Executable('./build.sh')
        build()

        with working_dir('build', create=True):
            if spec.satisfies('+cross-compile'):
                self.build_nmodl(spec, prefix)
            configure = Executable(join_path(self.stage.source_path, 'configure'))
            configure(*options)
            make()
            make('install')

    def setup_environment(self, spack_env, run_env):
        arch = self.get_arch_dir()
        run_env.prepend_path('PATH', join_path(self.prefix, arch, 'bin'))
