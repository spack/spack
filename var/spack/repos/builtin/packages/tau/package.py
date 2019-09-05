# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import fnmatch
import glob
import platform
from llnl.util.filesystem import join_path


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.28.1.tar.gz"
    git      = "https://github.com/UO-OACISS/tau2"

    version('develop', branch='master')
    version('2.28.2', '64e129a482056755012b91dae2fb4f728dbf3adbab53d49187eca952891c5457')
    version('2.28.1', '4e48fb477250f201ab00381cb43afea6')
    version('2.28', '68c6f13ae748d12c921456e494006796ca2b0efebdeef76ee7c898c81592883e')
    version('2.27.2p1', 'b9cc42ee8afdcfefe5104ab0a8f23a23')
    version('2.27.2', 'b264ab0df78112f9a529e59a5f4dc191')
    version('2.27.1', '4f98ff67ae5ab1ff2712f694bdec1fa9')
    version('2.27', '76602d35fc96f546b5b9dcaf09158651')
    version('2.26.3', '4ec14e85b8f3560b58628512c7b49e17')
    version('2.26.2', '8a5908c35dac9406c9220b8098c70c1c')
    version('2.26.1', 'cc13df9d6ad19bca9a8e55a9e7d0341e')
    version('2.26', '2af91f02ad26d5bf0954146c56a8cdfa')
    version('2.25', '46cd48fa3f3c4ce0197017b3158a2b43')
    version('2.24.1', '6635ece6d1f08215b02f5d0b3c1e971b')
    version('2.24', '57ce33539c187f2e5ec68f0367c76db4')
    version('2.23.1', '6593b47ae1e7a838e632652f0426fe72')

    variant('scorep', default=False, description='Activates SCOREP support')
    variant('openmp', default=False, description='Use OpenMP threads')
    variant('pthreads', default=True, description='Use POSIX threads')
    variant('mpi', default=False, description='Specify use of TAU MPI wrapper library')
    variant('phase', default=False, description='Generate phase based profiles')
    variant('papi', default=True, description='Activates Performance API')
    variant('binutils', default=True, description='Activates support of BFD GNU Binutils')
    variant('libdwarf', default=True, description='Activates support of libdwarf')
    variant('libelf', default=True, description='Activates support of libelf')
    variant('libunwind', default=True, description='Activates support of libunwind')
    variant('otf2', default=True, description='Activates support of Open Trace Format (OTF)')
    variant('pdt', default=True, description='Use PDT for source code instrumentation')
    variant('comm', default=False, description=' Generate profiles with MPI communicator info')
    variant('python', default=False, description='Activates Python support')
    variant('likwid', default=False, description='Activates LIKWID support')
    variant('ompt', default=False, description='Activates OMPT instrumentation')
    variant('opari', default=False, description='Activates Opari2 instrumentation')
    variant('shmem', default=False, description='Activates SHMEM support')
    variant('gasnet', default=False, description='Activates GASNET support')
    variant('cuda', default=False, description='Activates CUDA support')
    variant('fortran', default=True, description='Activates Fortran support')
    variant('io', default=True, description='Activates POSIX I/O support')

    # Support cross compiling.
    # This is a _reasonable_ subset of the full set of TAU
    # architectures supported:
    variant('craycnl', default=False, description='Build for Cray compute nodes')
    variant('bgq', default=False, description='Build for IBM BlueGene/Q compute nodes')
    variant('ppc64le', default=False, description='Build for IBM Power LE nodes')
    variant('x86_64', default=False, description='Force build for x86 Linux instead of auto-detect')

    depends_on('pdt', when='+pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    depends_on('otf2@2.1:', when='+otf2')
    depends_on('likwid', when='+likwid')
    depends_on('papi', when='+papi')
    depends_on('libdwarf', when='+libdwarf')
    depends_on('libelf', when='+libdwarf')
    # TAU requires the ELF header support, libiberty and demangle.
    depends_on('binutils+libiberty+headers~nls', when='+binutils')
    depends_on('python@2.7:', when='+python')
    depends_on('libunwind', when='+libunwind')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    depends_on('gasnet', when='+gasnet')

    # Elf only required from 2.28.1 on
    conflicts('+libelf', when='@:2.28.0')
    conflicts('+libdwarf', when='@:2.28.0')

    filter_compiler_wrappers('tau_cc.sh', 'Makefile.tau', relative_root='bin')

    def set_compiler_options(self, spec):

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

        compiler_options = ['-c++=%s' % os.path.basename(self.compiler.cxx),
                            '-cc=%s' % os.path.basename(self.compiler.cc)]

        if '+fortran' in spec and self.compiler.fc:
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

        if '+craycnl' in spec:
            options.append('-arch=craycnl')

        if '+bgq' in spec:
            options.append('-arch=bgq')

        if '+ppc64le' in spec:
            options.append('-arch=ibm64linux')

        if '+x86_64' in spec:
            options.append('-arch=x86_64')

        if ('platform=cray' in self.spec) and ('+x86_64' not in spec):
            options.append('-arch=craycnl')

        if '+pdt' in spec:
            options.append("-pdt=%s" % spec['pdt'].prefix)

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+pthreads' in spec:
            options.append('-pthread')

        if '+likwid' in spec:
            options.append("-likwid=%s" % spec['likwid'].prefix)

        if '+papi' in spec:
            options.append("-papi=%s" % spec['papi'].prefix)

        if '+openmp' in spec:
            options.append('-openmp')

        if '+opari' in spec:
            options.append('-opari')

        if '+ompt' in spec:
            options.append('-ompt')

        if '+io' in spec:
            options.append('-iowrapper')

        if '+binutils' in spec:
            options.append("-bfd=%s" % spec['binutils'].prefix)

        if '+libdwarf' in spec:
            options.append("-dwarf=%s" % spec['libdwarf'].prefix)

        if '+libelf' in spec:
            options.append("-elf=%s" % spec['libelf'].prefix)

        if '+libunwind' in spec:
            options.append("-unwind=%s" % spec['libunwind'].prefix)

        if '+otf2' in spec:
            options.append("-otf=%s" % spec['otf2'].prefix)

        if '+mpi' in spec:
            options.append('-mpi')
            if '+comm' in spec:
                options.append('-PROFILECOMMUNICATORS')

        if '+shmem' in spec:
            options.append('-shmem')

        if '+gasnet' in spec:
            options.append('-gasnet=%s' % spec['gasnet'].prefix)

        if '+cuda' in spec:
            options.append("-cuda=%s" % spec['cuda'].prefix)

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        if '+python' in spec:
            options.append('-python')
            # find Python.h (i.e. include/python2.7/Python.h)
            include_path = spec['python'].prefix.include
            found = False
            for root, dirs, files in os.walk(spec['python'].prefix.include):
                for filename in fnmatch.filter(files, 'Python.h'):
                    include_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythoninc=%s" % include_path)
            # find libpython*.* (i.e. lib/python2.7/libpython2.7.so)
            lib_path = spec['python'].prefix.lib
            found = False
            file_to_find = 'libpython*.so'
            if (platform.system() == "Darwin"):
                file_to_find = 'libpython*.dylib'
            for root, dirs, files in os.walk(spec['python'].prefix.lib):
                for filename in fnmatch.filter(files, file_to_find):
                    lib_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythonlib=%s" % lib_path)

        compiler_specific_options = self.set_compiler_options(spec)
        options.extend(compiler_specific_options)
        configure(*options)
        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()

    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ('bin', 'lib'):
                src = join_path(self.prefix, subdir, d)
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
