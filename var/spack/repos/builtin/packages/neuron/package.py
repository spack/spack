##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
from spack import *


class Neuron(Package):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments. The primary scripting
    language is hoc but a Python interface is also available.
    """

    homepage = "https://www.neuron.yale.edu/"
    url      = "http://www.neuron.yale.edu/ftp/neuron/versions/v7.5/nrn-7.5.tar.gz"
    github   = "https://github.com/nrnhines/nrn"

    version('7.5', 'fb72c841374dfacbb6c2168ff57bfae9')
    version('7.4', '2c0bbee8a9e55d60fa26336f4ab7acbf')
    version('7.3', '993e539cb8bf102ca52e9fefd644ab61')
    version('7.2', '5486709b6366add932e3a6d141c4f7ad')
    version('develop', git=github, preferred=True)

    variant('binary',        default=True, description="Create special as a binary instead of shell script")
    variant('coreneuron',    default=True, description="Patch hh.mod for CoreNEURON compatibility")
    variant('cross-compile', default=False, description='Build for cross-compile environment')
    variant('debug',         default=False, description='Build debug with O0')
    variant('mpi',           default=True,  description='Enable MPI parallelism')
    variant('multisend',     default=True,  description="Enable multi-send spike exchange")
    variant('profile',       default=False, description="Enable Tau profiling")
    variant('python',        default=True,  description='Enable python')
    variant('shared',        default=True, description='Build shared libraries')
    variant('rx3d',          default=False, description="Enable cython translated 3-d rxd")

    depends_on('autoconf',   type='build')
    depends_on('automake',   type='build')
    depends_on('bison',      type='build')
    depends_on('flex',       type='build')
    depends_on('libtool',    type='build')
    depends_on('pkg-config', type='build')

    depends_on('mpi',         when='+mpi')
    depends_on('ncurses',     when='~cross-compile')
    depends_on('python@2.6:', when='+python')
    depends_on('tau',         when='+profile')

    conflicts('~shared', when='+python')

    filter_compiler_wrappers('*/bin/nrniv_makefile')

    def get_neuron_archdir(self):
        """Determine the architecture-specific neuron base directory.

        Instead of recreating the logic of the neuron's configure
        we dynamically find the architecture-specific directory by
        looking for a specific binary.
        """
        file_list = find(self.prefix, '*/bin/nrniv_makefile')
        # check needed as when initially evaluated the prefix is empty
        if file_list:
            neuron_archdir = os.path.dirname(os.path.dirname(file_list[0]))
        else:
            neuron_archdir = self.prefix

        return neuron_archdir

    def patch(self):
        # aclocal need complete include path (especially on os x)
        pkgconf_inc = '-I %s/share/aclocal/' % (self.spec['pkg-config'].prefix)
        libtool_inc = '-I %s/share/aclocal/' % (self.spec['libtool'].prefix)
        newpath = 'aclocal -I m4 %s %s' % (pkgconf_inc, libtool_inc)
        filter_file(r'aclocal -I m4', r'%s' % newpath, "build.sh")

        # patch hh.mod to be compatible with coreneuron
        if self.spec.satisfies('+coreneuron'):
            filter_file(r'GLOBAL minf', r'RANGE minf', 'src/nrnoc/hh.mod')
            filter_file(r'TABLE minf', r':TABLE minf', "src/nrnoc/hh.mod")

    def profiling_wrapper_on(self):
        os.environ["USE_PROFILER_WRAPPER"] = "1"

    def profiling_wrapper_off(self):
        del os.environ["USE_PROFILER_WRAPPER"]

    def get_arch_options(self, spec):
        options = []

        if spec.satisfies('+cross-compile'):
            options.extend(['cross_compiling=yes',
                            '--without-memacs',
                            '--without-nmodl'])
        # need to enable bg-q arch
        if 'bgq' in self.spec.architecture:
            options.extend(['--enable-bluegeneQ',
                            '--host=powerpc64'])

        # on os-x disable building carbon 'click' utility
        if 'darwin' in self.spec.architecture:
            options.append('macdarwin=no')

        return options

    def get_python_options(self, spec):
        options = []

        if spec.satisfies('+python'):
            python_exec = spec['python'].command.path
            py_inc = spec['python'].headers.directories[0]
            py_lib = spec['python'].prefix.lib

            if not os.path.isdir(py_lib):
                py_lib = spec['python'].prefix.lib64

            options.extend(['--with-nrnpython=%s' % python_exec,
                            '--disable-pysetup',
                            'PYINCDIR=%s' % py_inc,
                            'PYLIBDIR=%s' % py_lib])

            if spec.satisfies('~cross-compile'):
                options.append('PYTHON_BLD=%s' % python_exec)

        else:
            options.append('--without-nrnpython')

        return options

    def get_compiler_options(self, spec):
        flags = '-O2 -g'

        if 'bgq' in spec.architecture:
            flags = '-O3 -qtune=qp -qarch=qp -q64 -qstrict -qnohot -g'

        if spec.satisfies('+debug'):
            flags = '-g -O0'

        if self.spec.satisfies('%pgi'):
            flags += ' ' + self.compiler.pic_flag

        return ['CFLAGS=%s' % flags,
                'CXXFLAGS=%s' % flags]

    def build_nmodl(self, spec, prefix):
        # build components for front-end arch in cross compiling environment
        options = ['--prefix=%s' % prefix,
                   '--with-nmodl-only',
                   '--without-x']

        if 'bgq' in self.spec.architecture:
            flags = '-qarch=ppc64'
            options.extend(['CFLAGS=%s' % flags,
                            'CXXFLAGS=%s' % flags])

        if 'cray' in self.spec.architecture:
            flags = '-target-cpu=x86_64 -target-network=none'
            options.extend(['CFLAGS=%s' % flags,
                            'CXXFLAGS=%s' % flags])

        configure = Executable(join_path(self.stage.source_path, 'configure'))
        configure(*options)
        make()
        make('install')

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix,
                   '--without-iv',
                   '--without-x',
                   '--without-readline']

        if spec.satisfies('+multisend'):
            options.append('--with-multisend')

        if spec.satisfies('~rx3d'):
            options.append('--disable-rx3d')

        if spec.satisfies('+mpi'):
            options.extend(['MPICC=%s' % spec['mpi'].mpicc,
                            'MPICXX=%s' % spec['mpi'].mpicxx,
                            '--with-paranrn'])
        else:
            options.append('--without-paranrn')

        if spec.satisfies('~shared'):
            options.append('--disable-shared')

        if spec.satisfies('+binary'):
            options.append('linux_nrnmech=no')

        options.extend(self.get_arch_options(spec))
        options.extend(self.get_python_options(spec))
        options.extend(self.get_compiler_options(spec))

        # -M option to Tau disables instrumentation
        if spec.satisfies('+profile'):
            options.extend(['--disable-dependency-tracking',
                            'CC=%s' % 'tau_cc',
                            'CXX=%s' % 'tau_cxx',
                            'MPICC=%s' % 'tau_cc',
                            'MPICXX=%s' % 'tau_cxx'])

        build = Executable('./build.sh')
        build()

        with working_dir('build', create=True):
            if spec.satisfies('+cross-compile'):
                self.build_nmodl(spec, prefix)
            srcpath = self.stage.source_path
            configure = Executable(join_path(srcpath, 'configure'))
            configure(*options)
            self.profiling_wrapper_on()
            make('VERBOSE=1')
            make('install')
            self.profiling_wrapper_off()

    @run_after('install')
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        arch = self.get_neuron_archdir()
        nrnmakefile = join_path(self.prefix, arch, 'bin/nrniv_makefile')

        kwargs = {
            'backup': False,
            'string': True
        }

        filter_file(env['CC'],  self.compiler.cc, nrnmakefile, **kwargs)
        filter_file(env['CXX'], self.compiler.cxx, nrnmakefile, **kwargs)

    def setup_environment(self, spack_env, run_env):
        neuron_archdir = self.get_neuron_archdir()
        run_env.prepend_path('PATH', join_path(neuron_archdir, 'bin'))
        run_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        neuron_archdir = self.get_neuron_archdir()
        spack_env.prepend_path('PATH', join_path(neuron_archdir, 'bin'))
        spack_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))

    def setup_dependent_package(self, module, dependent_spec):
        neuron_archdir = self.get_neuron_archdir()
        dependent_spec.package.neuron_archdir = neuron_archdir
