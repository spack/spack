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
import os
import glob
from llnl.util.filesystem import join_path


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.25.tar.gz"

    version('2.25', '46cd48fa3f3c4ce0197017b3158a2b43')
    version('2.24.1', '6635ece6d1f08215b02f5d0b3c1e971b')
    version('2.24', '57ce33539c187f2e5ec68f0367c76db4')
    version('2.23.1', '6593b47ae1e7a838e632652f0426fe72')

    # TODO : shmem variant missing
    variant('download', default=False,
            description='Downloads and builds various dependencies')
    variant('scorep', default=False, description='Activates SCOREP support')
    variant('openmp', default=True, description='Use OpenMP threads')
    variant('mpi', default=True,
            description='Specify use of TAU MPI wrapper library')
    variant('phase', default=True, description='Generate phase based profiles')
    variant('comm', default=True,
            description=' Generate profiles with MPI communicator info')

    # TODO : Try to build direct OTF2 support? Some parts of the OTF support
    # TODO : library in TAU are non-conformant,
    # TODO : and fail at compile-time. Further, SCOREP is compiled with OTF2
    # support.
    depends_on('pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    depends_on('binutils', when='~download')
    depends_on('mpi', when='+mpi')

    def set_compiler_options(self):

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
                   "-iowrapper",
                   "-pdt=%s" % spec['pdt'].prefix]
        # If download is active, download and build suggested dependencies
        if '+download' in spec:
            options.extend(['-bfd=download',
                            '-unwind=download',
                            '-asmdex=download'])
        else:
            options.extend(["-bfd=%s" % spec['binutils'].prefix])
            # TODO : unwind and asmdex are still missing

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+openmp' in spec:
            options.append('-openmp')

        if '+mpi' in spec:
            options.append('-mpi')

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        if '+comm' in spec:
            options.append('-PROFILECOMMUNICATORS')

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
