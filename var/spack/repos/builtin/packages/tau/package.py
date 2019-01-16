# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob
from llnl.util.filesystem import join_path


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.28.tar.gz"
    git      = "https://github.com/UO-OACISS/tau2"

    version('develop', branch='master')
    version('2.28', '68c6f13ae748d12c921456e494006796ca2b0efebdeef76ee7c898c81592883e')
    version('2.27.1', '4f98ff67ae5ab1ff2712f694bdec1fa9')
    version('2.27',   '76602d35fc96f546b5b9dcaf09158651')
    version('2.26.3', '4ec14e85b8f3560b58628512c7b49e17')
    version('2.25', '46cd48fa3f3c4ce0197017b3158a2b43')
    version('2.24.1', '6635ece6d1f08215b02f5d0b3c1e971b')
    version('2.24', '57ce33539c187f2e5ec68f0367c76db4')
    version('2.23.1', '6593b47ae1e7a838e632652f0426fe72')

    # TODO : shmem variant missing
    variant('scorep', default=False, description='Activates SCOREP support')
    variant('openmp', default=True, description='Use OpenMP threads')
    variant('mpi', default=True,
            description='Specify use of TAU MPI wrapper library')
    variant('phase', default=True, description='Generate phase based profiles')
    variant('papi', default=True, description='Use PAPI for hardware counters')
    variant('binutils', default=True, description='Use Binutils for address resolution')
    variant('libunwind', default=True, description='Use Libunwind for call stack unwinding')
    variant('otf2', default=True, description='Use OTF2 for trace format output')
    variant('pdt', default=True, description='Use PDT for source code instrumentation')
    variant('comm', default=True,
            description=' Generate profiles with MPI communicator info')

    depends_on('pdt', when='+pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    depends_on('papi', when='+papi')
    depends_on('binutils+libiberty~nls', when='+binutils')
    depends_on('libunwind', when='+libunwind')
    depends_on('otf2', when='+otf2')
    depends_on('mpi', when='+mpi')

    def set_compiler_options(self):

        useropt = ["-O2 -g", self.rpath_args]

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
        if self.compiler.fc:
            compiler_options.append('-fortran=%s' % self.compiler.fc_names[0])
        ##########

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
                   "-iowrapper"]

        if '+pdt' in spec:
            options.append("-pdt=%s" % spec['pdt'].prefix)

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+openmp' in spec:
            options.append('-openmp')

        if '+papi' in spec:
            options.append("-papi=%s" % spec['papi'].prefix)

        if '+binutils' in spec:
            options.append("-bfd=%s" % spec['binutils'].prefix)

        if '+libunwind' in spec:
            options.append("-unwind=%s" % spec['libunwind'].prefix)

        if '+otf2' in spec:
            options.append("-otf=%s" % spec['otf2'].prefix)

        if '+mpi' in spec:
            options.append('-mpi')
            if '+comm' in spec:
                options.append('-PROFILECOMMUNICATORS')

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        compiler_specific_options = self.set_compiler_options()
        options.extend(compiler_specific_options)
        configure(*options)
        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()

    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ('bin', 'lib'):
                src  = join_path(self.prefix, subdir, d)
                dest = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dest):
                    os.symlink(join_path(subdir, d), dest)

    def setup_environment(self, spack_env, run_env):
        pattern = join_path(self.prefix.lib, 'Makefile.*')
        files = glob.glob(pattern)

        # This function is called both at install time to set up
        # the build environment and after install to generate the associated
        # module file. In the former case there is no `self.prefix.lib`
        # directory to inspect. The conditional below will set `TAU_MAKEFILE`
        # in the latter case.
        if files:
            run_env.set('TAU_MAKEFILE', files[0])
