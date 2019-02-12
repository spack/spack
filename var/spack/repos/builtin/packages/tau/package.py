# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import stat
import sys
import glob
from llnl.util.filesystem import join_path


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.25.tar.gz"

    version('2.27.1', '4f98ff67ae5ab1ff2712f694bdec1fa9')
    version('2.27',   '76602d35fc96f546b5b9dcaf09158651')
    version('2.26.3', '4ec14e85b8f3560b58628512c7b49e17')
    version('2.26.2', '8a5908c35dac9406c9220b8098c70c1c')
    version('2.25',   '46cd48fa3f3c4ce0197017b3158a2b43')
    version('2.24.1', '6635ece6d1f08215b02f5d0b3c1e971b')
    version('2.24',   '57ce33539c187f2e5ec68f0367c76db4')
    version('2.23.1', '6593b47ae1e7a838e632652f0426fe72')

    # TODO : shmem variant missing
    variant('download', default=False,
            description='Downloads and builds various dependencies')
    variant('scorep', default=False, description='Activates SCOREP support')
    variant('openmp', default=True, description='Use OpenMP threads')
    variant('pthread', default=False, description='Activates Pthread support')
    variant('mpi', default=True,
            description='Specify use of TAU MPI wrapper library')
    variant('phase', default=True, description='Generate phase based profiles')
    # TODO : comm variant has bug, reported upstream
    variant('comm', default=False,
            description=' Generate profiles with MPI communicator info')
    variant('ompt', default=False, description='Use OpenMP tool interface (with Intel compiler)')

    # TODO : Try to build direct OTF2 support? Some parts of the OTF support
    # TODO : library in TAU are non-conformant,
    # TODO : and fail at compile-time. Further, SCOREP is compiled with OTF2
    # support.
    depends_on('pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    #depends_on('binutils', when='~download')
    depends_on('mpi', when='+mpi')

    def patch(self):
        # TODO : neuron autotools add -MD option which turns off tau profile
        filter_file(r' -M', r' -Q', 'tools/src/tau_cc.sh')
        filter_file(r' -M', r' -Q', 'tools/src/tau_cxx.sh')

    def set_compiler_options(self, spec):

        useropt = ["-O2", self.rpath_args]

        ##########
        # Selecting a compiler with TAU configure is quite tricky:
        # 1 - compilers are mapped to a given set of strings
        #     (and spack cc, cxx, etc. wrappers are not among them)
        # 2 - absolute paths are not allowed
        # 3 - the usual environment variables seems not to be checked
        #     ('CC', 'CXX' and 'FC')
        # 4 - if no -cc=<compiler> -cxx=<compiler> is passed tau is built with
        #     system compiler silently
        # (regardless of what %<compiler> is used in the spec)
        #
        # In the following we give TAU what he expects and put compilers into
        # PATH
        compiler_path = os.path.dirname(self.compiler.cc)
        os.environ['PATH'] = ':'.join([compiler_path, os.environ['PATH']])
        compiler_options = ['-c++=%s' % self.compiler.cxx_names[0],
                            '-cc=%s' % self.compiler.cc_names[0]]

        # TODO : Handle other compilers (tau except vendor name for fortran)
        if self.compiler.fc:
            if spec.satisfies('%intel'):
                compiler_options.append('-fortran=intel')
            elif spec.satisfies('%pgi'):
                # @bbp we don't have pgfortran but fc is set to gfortran in packages.yaml
                # to compiler mpi libraries
                pass
            else:
                compiler_options.append('-fortran=%s' % self.compiler.fc_names[0])
        ##########

        # on bg-q we dont need compiler names. We also have to set fortran
        # because spack set EXTRADIRCXX spack wrapper directory and then
        # tau use relative path to find fortran link libraries.
        if 'bgq' in spec.architecture and spec.satisfies('%xl'):
            compiler_options = ['-pdt_c++=xlC']

        # Construct the string of custom compiler flags and append it to
        # compiler related options
        useropt = ' '.join(useropt)
        useropt = "-useropt=%s" % useropt
        compiler_options.append(useropt)
        return compiler_options

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.
        change_sed_delimiter('@', ';', 'configure')
        change_sed_delimiter('@', ';', 'utils/FixMakefile')
        change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')

        # TAU configure, despite the name , seems to be a manually
        # written script (nothing related to autotools).  As such it has
        # a few #peculiarities# that make this build quite hackish.
        options = ["-prefix=%s" % prefix,
                   "-iowrapper",
                   "-pdt=%s" % spec['pdt'].prefix]
        # If download is active, download and build suggested dependencies
        if '+download' in spec:
            options.extend(['-bfd=download',
                            '-unwind=download',
                            '-asmdex=download'])
        #else:
        #    options.extend(["-bfd=%s" % spec['binutils'].prefix])
            # TODO : unwind and asmdex are still missing

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+openmp' in spec:
            options.extend(['-openmp', '-opari'])

        if '+pthread' in spec:
            options.append('-pthread')

        if '+mpi' in spec:
            options.append('-mpi')

            # see #5320, need to see if we cleanup a bit with one logic as
            # headers.directories is generic
            if spec.satisfies('^intel-mpi') or spec.satisfies('^intel-parallel-studio'):
                options.append('-mpiinc=%s' % spec['mpi'].headers.directories[0])
            else:
                options.append('-mpiinc=%s' % spec['mpi'].prefix.include)
                options.append('-mpilib=%s' % spec['mpi'].prefix.lib)

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        if '+comm' in spec:
            options.append('-PROFILECOMMUNICATORS')

        if '+ompt' in spec:
            if self.compiler.name == 'intel':
                options.append('-ompt=download')
            else:
                raise InstallError('OMPT supported only with Intel compiler!')

        if 'bgq' in spec.architecture:
            options.extend(['-arch=bgq', '-BGQTIMERS'])
        elif 'cray' in spec.architecture:
            options.append('-arch=craycnl')
        elif 'x86_64' in spec.architecture:
            options.append('-arch=x86_64')

        # latest 2.26.2 version doesnt build on osx with plugins
        # also seeing this issue on bg-q
        if spec.satisfies('@2.26.2:'):
            options.append('-noplugins')

        compiler_specific_options = self.set_compiler_options(spec)
        options.extend(compiler_specific_options)
        configure(*options)
        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()

        # create tau compiler wrappers
        self.create_tau_compiler_wrapper()

    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ('bin', 'lib'):
                src  = join_path(self.prefix, subdir, d)
                dest = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dest):
                    os.symlink(join_path(subdir, d), dest)

    def create_tau_compiler_wrapper(self):
        c_compiler = self.compiler.cc
        cxx_compiler = self.compiler.cxx

        if '+mpi' in self.spec:
            c_compiler = self.spec['mpi'].mpicc
            cxx_compiler = self.spec['mpi'].mpicxx

        compilers = {'tau_cc': 'tau_cc.sh', 'tau_cxx': 'tau_cxx.sh'}

        spack_compilers = {'tau_cc': c_compiler,
                           'tau_cxx': cxx_compiler}

        for tau_wrapper_compiler, tau_compiler in compilers.items():
            fname = join_path(self.prefix.bin, tau_wrapper_compiler)
            f = open(fname, 'w')
            content = 'if [ -n "${USE_PROFILER_WRAPPER}" ]; then' + '\n'
            content += '    %s $PROFILER_FLAGS "$@"' % tau_compiler + '\n'
            content += 'else' + '\n'
            content += '    %s "$@"' % spack_compilers[tau_wrapper_compiler] + '\n'
            content += 'fi'
            f.write(content)
            f.close()
            chmod = which('chmod')
            chmod('ugo+rx', fname)

    def get_makefiles(self):
        pattern = join_path(self.prefix.lib, 'Makefile.*')
        return glob.glob(pattern)

    def setup_environment(self, spack_env, run_env):
        files = self.get_makefiles()

        # This function is called both at install time to set up
        # the build environment and after install to generate the associated
        # module file. In the former case there is no `self.prefix.lib`
        # directory to inspect. The conditional below will set `TAU_MAKEFILE`
        # in the latter case.
        if files:
            run_env.set('TAU_MAKEFILE', files[0])

    def setup_dependent_environment(self, module, spec, dep_spec):
        files = self.get_makefiles()
        os.environ['TAU_MAKEFILE'] = files[0] if files else ''

    @run_after('install')
    def filter_compilers(self):

        makefile = self.get_makefiles()[0]

        if 'bgq' in self.spec.architecture and self.spec.satisfies('%xl'):
            # tau links to some fortran libraries which are located in
            # /opt/ibmcmp/xlf/bg/14.1/bglib64/. Spack set fortran wrappers
            # which tau use. But Tau also use wrapper path to get path
            # of /opt/ibmcmp/xlf/bg/14.1/bglib64. But it use wrappers
            # path which obviously break the links. For now get path from
            # SPACK_FC and patch Makefile.
            fc = os.environ['SPACK_FC']
            extra_dir = os.path.dirname(os.path.dirname(fc))
            filter_file(r'EXTRADIR=.*', r'EXTRADIR=%s' % extra_dir, makefile)

        if 'cray' in self.spec.architecture:
            makefile = self.get_makefiles()[0]
            filter_file(r'FULL_CC=.*', r'FULL_CC=%s' % self.compiler.cc, makefile)
            filter_file(r'FULL_CXX=.*', r'FULL_CXX=%s' % self.compiler.cxx, makefile)
