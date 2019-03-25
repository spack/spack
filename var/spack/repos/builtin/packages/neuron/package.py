# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *
from contextlib import contextmanager


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
    git      = "https://github.com/nrnhines/nrn.git"

    version('develop', branch='master')
    version('2018-10', commit='b3097b7', preferred=True)
    version('2018-09', commit='9f36b13')
    version('7.6.2',   tag='7.6.2')
    # versions from url, with checksum
    version('7.5', 'fb72c841374dfacbb6c2168ff57bfae9')
    version('7.4', '2c0bbee8a9e55d60fa26336f4ab7acbf')
    version('7.3', '993e539cb8bf102ca52e9fefd644ab61')
    version('7.2', '5486709b6366add932e3a6d141c4f7ad')

    variant('binary',        default=True,  description="Create special as a binary instead of shell script")
    variant('coreneuron',    default=True,  description="Patch hh.mod for CoreNEURON compatibility")
    variant('cross-compile', default=False, description='Build for cross-compile environment')
    variant('debug',         default=False, description='Build debug with O0')
    variant('mpi',           default=True,  description='Enable MPI parallelism')
    variant('multisend',     default=True,  description="Enable multi-send spike exchange")
    variant('profile',       default=False, description="Enable Tau profiling")
    variant('python',        default=True,  description='Enable python')
    variant('shared',        default=True,  description='Build shared libraries')
    variant('pysetup',       default=True,  description="Build Python module with setup.py")
    variant('rx3d',          default=False, description="Enable cython translated 3-d rxd. Depends on pysetup")

    depends_on('autoconf',   type='build')
    depends_on('automake',   type='build')
    depends_on('bison',      type='build')
    depends_on('flex',       type='build')
    depends_on('libtool',    type='build')
    depends_on('pkgconfig',  type='build')

    depends_on('readline')
    depends_on('mpi',         when='+mpi')
    depends_on('ncurses',     when='~cross-compile')
    depends_on('python@2.6:', when='+python', type=('build', 'link', 'run'))
    depends_on('tau',         when='+profile')

    conflicts('~shared',  when='+python')
    conflicts('+pysetup', when='~python')
    conflicts('+rx3d',    when='~pysetup')

    _default_options = ['--without-iv',
                        '--without-x']
    _specs_to_options = {
        '+cross-compile': ['cross_compiling=yes',
                           '--without-memacs',
                           '--without-nmodl'],
        '~python':    ['--without-nrnpython'],
        '~pysetup':   ['--disable-pysetup'],
        '+mpi+multisend': ['--with-multisend'],
        '~rx3d':      ['--disable-rx3d'],
        '~mpi':       ['--without-paranrn'],
        '+mpi':       ['--with-paranrn'],
        '~shared':    ['--disable-shared'],
        '+binary':    ['linux_nrnmech=no'],
    }

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
        pkgconf_inc = '-I %s/share/aclocal/' % (self.spec['pkgconfig'].prefix)
        libtool_inc = '-I %s/share/aclocal/' % (self.spec['libtool'].prefix)
        newpath = 'aclocal -I m4 %s %s' % (pkgconf_inc, libtool_inc)
        filter_file(r'aclocal -I m4', r'%s' % newpath, "build.sh")

        # patch hh.mod to be compatible with coreneuron
        if self.spec.satisfies('+coreneuron'):
            filter_file(r'GLOBAL minf', r'RANGE minf', 'src/nrnoc/hh.mod')
            filter_file(r'TABLE minf', r':TABLE minf', "src/nrnoc/hh.mod")

    def get_arch_options(self, spec):
        options = []
        # need to enable bg-q arch
        if 'bgq' in self.spec.architecture:
            options.extend(['--enable-bluegeneQ',
                            '--host=powerpc64'])

        # on os-x disable building carbon 'click' utility
        if 'darwin' in self.spec.architecture:
            options.append('macdarwin=no')

        return options

    def get_python_options(self, spec):
        """Determine config options for Python
        """
        options = []

        if spec.satisfies('+python'):
            python_exec = spec['python'].command.path
            py_inc = spec['python'].headers.directories[0]
            py_lib = spec['python'].prefix.lib

            if not os.path.isdir(py_lib):
                py_lib = spec['python'].prefix.lib64

            options.extend(['--with-nrnpython=%s' % python_exec,
                            'PYINCDIR=%s' % py_inc,
                            'PYLIBDIR=%s' % py_lib])

            # use python dependency if not cross-compiling or on cray system
            if spec.satisfies('~cross-compile') or 'cray' in spec.architecture:
                options.append('PYTHON_BLD=%s' % python_exec)

        return options

    def get_compilation_options(self, spec):
        """ Build options setting compilers and compilation flags,
            using MPIC[XX] and C[XX]FLAGS
        """
        flags = '-O2 -g'

        if 'bgq' in spec.architecture:
            flags = '-O3 -qtune=qp -qarch=qp -q64 -qstrict -qnohot -g'

        if spec.satisfies('+debug'):
            flags = '-g -O0'

        if self.spec.satisfies('%pgi'):
            flags += ' ' + self.compiler.pic_flag

        options = ['CFLAGS=%s' % flags,
                   'CXXFLAGS=%s' % flags]

        if spec.satisfies('+profile'):
            options.extend(['--disable-dependency-tracking',
                            'CC=%s' % 'tau_cc',
                            'CXX=%s' % 'tau_cxx'])
            if spec.satisfies('+mpi'):
                options.extend(['MPICC=%s' % 'tau_cc',
                                'MPICXX=%s' % 'tau_cxx'])
        elif spec.satisfies('+mpi'):
            options.extend(['MPICC=%s' % spec['mpi'].mpicc,
                            'MPICXX=%s' % spec['mpi'].mpicxx])
        return options

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
        options = ['--prefix=%s' % prefix] + self._default_options
        for specname, spec_opts in self._specs_to_options.items():
            if spec.satisfies(specname):
                options.extend(spec_opts)

        options.extend(self.get_arch_options(spec))
        options.extend(self.get_python_options(spec))
        options.extend(self.get_compilation_options(spec))

        options.append('--with-readline=%s' % spec['readline'].prefix)
        ld_flags = 'LDFLAGS=-L{0.prefix.lib} {0.libs.rpath_flags}'.format(spec['readline'])

        if 'ncurses' in spec:
            options.extend(['CURSES_LIBS=%s' % spec['ncurses'].libs.ld_flags,
                            'CURSES_CFLAGS=%s' % spec['ncurses'].prefix.include])
            ld_flags += ' -L{0.prefix.lib} {0.libs.rpath_flags}'.format(spec['ncurses'])

        options.append(ld_flags)

        build = Executable('./build.sh')
        build()

        with working_dir('build', create=True):
            if spec.satisfies('+cross-compile'):
                self.build_nmodl(spec, prefix)
            srcpath = self.stage.source_path
            configure = Executable(join_path(srcpath, 'configure'))
            configure(*options)
            with profiling_wrapper_on():
                make('VERBOSE=1')
                make('install')

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
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))
        if self.spec.satisfies('+pysetup'):
            run_env.prepend_path('PYTHONPATH', self.spec.prefix.lib64.python)
            run_env.prepend_path('PYTHONPATH', self.spec.prefix.lib.python)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        neuron_archdir = self.get_neuron_archdir()
        spack_env.prepend_path('PATH', join_path(neuron_archdir, 'bin'))
        spack_env.prepend_path('LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))
        if self.spec.satisfies('+python'):
            run_env.prepend_path('PYTHONPATH', self.spec.prefix.lib64.python)
            run_env.prepend_path('PYTHONPATH', self.spec.prefix.lib.python)

    def setup_dependent_package(self, module, dependent_spec):
        neuron_archdir = self.get_neuron_archdir()
        dependent_spec.package.neuron_archdir = neuron_archdir


@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]

