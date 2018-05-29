##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os
import glob
from llnl.util.filesystem import join_path
import subprocess as sp
import json

class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """
    
    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.27.1.tar.gz"

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

    # TODO : shmem variant missing
    variant('download', default=False,
            description='Downloads and builds various dependencies')
    variant('scorep', default=False, description='Activates SCOREP support')
    variant('otf', default=False, description='Activates support of Open Trace Format (OTF)')
    variant('binutils', default=False, description='Activates support of BFD GNU Binutils')
    variant('libunwind', default=False, description='Activates support of libunwind')
    variant('likwid', default=False, description='Activates LIKWID support')
    variant('papi', default=True, description='Activates Performance API')
    variant('python', default=True, description='Activates Python support')
    variant('openmp', default=False, description='Use OpenMP threads')
    variant('ompt', default=False, description='Activates OMPT instrumentation')
    variant('opari', default=False, description='Activates Opari2 instrumentation')
    variant('mpi', default=True,
            description='Specify use of TAU MPI wrapper library')
    variant('phase', default=False, description='Generate phase based profiles')
    variant('comm', default=False,
            description=' Generate profiles with MPI communicator info')
    variant('shmem', default=False,
             description='Activates SHMEM support')
    variant('gasnet', default=False,
             description='Activates GASNET support')
    variant('cuda', default=False,
             description='Activates CUDA support')
    variant('beacon', default=False, description='Activates BEACON support')
    
 
    # Check MPI implementation
    #try:
    #  mpirunOut = os.popen('which mpirun')
    #except OSError as e:
    #  print "OSError > ", e.errno
    #  print "OSError > ", e.strerror
   
    mpiruncmd = "which mpirun" 
    ret = sp.call(mpiruncmd, shell=True)
    if ret != 0:
      print "mpirun does not exist - reading from JSON file"
      strmpijson = ""
      with open('/dev/shm/mpi.json') as mpi_file:
        data = json.load(mpi_file)
      print(data)
      strmpijson = data["mpi"]

      if "mpich" in strmpijson:
        print "mpich in JSON file"
        MpiImpl = 'mpich'
      elif "mvapich2" in strmpijson:
        print "mvapich2 in JSON file"
        MpiImpl = 'mvapich2'
      elif "openmpi" in strmpijson:
        print "openmpi in JSON file"
        MpiImpl = 'openmpi'
      elif "intel" in strmpijson:
        print "IntelMpi in JSON file"
        MpiImpl = 'intel-mpi'

    else:
      print "mpirun exists"
      #strMpiImplOut = sp.Popen(["which", "mpirun"],stdout=sp.PIPE)
      #print p.communicate
      
      #strMpiImplOut = sp.Popen(["which", "mpirun"],stdout=sp.PIPE)
      mpirunOut = os.popen('which mpirun')
      #strMpiImplOut = os.popen('which mpirun').read() 
      strMpiImplOut = mpirunOut.read()
      #print "Mpi Impl out: ", strMpiImplOut
      #MpiImpl = "mpich"
      if "mpich" in strMpiImplOut:
        MpiImpl = 'mpich'
      elif "mvapich2" in strMpiImplOut:
        MpiImpl = 'mvapich2'
      elif "openmpi" in strMpiImplOut:
        MpiImpl = 'openmpi'
      elif "intel" in strMpiImplOut:
        MpiImpl = 'intel-mpi'
      #else:
      #  MpiImpl = ""

        # TODO : Try to build direct OTF2 support? Some parts of the OTF support
    # TODO : library in TAU are non-conformant,
    # TODO : and fail at compile-time. Further, SCOREP is compiled with OTF2
    # support.
    depends_on('pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    depends_on('otf2@2.1', when='+otf')
    depends_on('likwid', when='+likwid')
    depends_on('papi', when='+papi')
    depends_on('python', when='+python')
    #depends_on('binutils', when='~download')
    depends_on('gettext')
    depends_on('binutils@2.27+libiberty')
    depends_on('libunwind', when='~download')
    depends_on(MpiImpl, when='+mpi')
    depends_on("mpi", when='+mpi')
    depends_on('cuda', when='+cuda')
    depends_on('gasnet', when='+gasnet')

    #filter_compiler_wrappers(
    #    'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpifort', relative_root='bin'
    #)

    filter_compiler_wrappers('tau_cc.sh', 'Makefile.tau', relative_root='bin')

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

        #compiler_options = []
        compiler_options = ['-c++=%s' % self.compiler.cxx,
                            '-cc=%s' % self.compiler.cc]

        #compiler_options = ['-c++=mpicxx',
        #                    '-cc=mpicc']

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

#	 print "export SPACK_PREFIX=",os.environ['SPACK_PREFIX']
#        print "export SPACK_ENV_PATH=",os.environ['SPACK_ENV_PATH']
#        print "export SPACK_DEBUG_LOG_DIR=",os.environ['SPACK_DEBUG_LOG_DIR']
#        print "export SPACK_DEBUG_LOG_ID=",os.environ['SPACK_DEBUG_LOG_ID']
#        print "export SPACK_COMPILER_SPEC=",os.environ['SPACK_COMPILER_SPEC']
#        print "export SPACK_CC_RPATH_ARG=",os.environ['SPACK_CC_RPATH_ARG']
#        print "export SPACK_CXX_RPATH_ARG=",os.environ['SPACK_CXX_RPATH_ARG']
#        print "export SPACK_F77_RPATH_ARG=",os.environ['SPACK_F77_RPATH_ARG']
#        print "export SPACK_FC_RPATH_ARG=",os.environ['SPACK_FC_RPATH_ARG']
#        print "export SPACK_SHORT_SPEC=",os.environ['SPACK_SHORT_SPEC']

        options.extend(["-bfd=%s" % spec['binutils'].prefix])
        #options.extend(["-bfd=/home/users/sameer/tau-2.27.1/x86_64/binutils-2.23.2"])
        options.extend(["-unwind=%s" % spec['libunwind'].prefix])
	#if '+binutils' in spec:
        #    options.extend(["-bfd=%s" % spec['binutils'].prefix])
        #else:
        #    options.extend(['-bfd=download'])
	#if '+libunwind' in spec:
        #    options.extend(["-unwind=%s" % spec['libunwind'].prefix])
        #else:
        #    options.extend(['-unwind=download'])
	#if '+otf' in spec:
        #    options.extend(["-otf=%s" % spec['otf'].prefix])
        #else:
        #    options.extend(['-otf=download'])

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+likwid' in spec:
            options.append("-likwid=%s" % spec['likwid'].prefix)

        if '+papi' in spec:
            options.append("-papi=%s" % spec['papi'].prefix)

        if '+python' in spec:
            options.append("-python")

        if '+openmp' in spec:
            options.append('-openmp')

        if '+opari' in spec:
            options.append('-opari')

        if '+mpi' in spec: 
            print "MPI in spec"
            strMpiIncTmp = ""
            strMpiLibsTmp = ""
            strMpiLibraryTmp = ""
            strMpi = os.popen('mpicc -show').read()
            print "mpicc -show: ", strMpi
            #parse_mpi_wrapper(strmpi) 
            listMpiOpts = strMpi.split()
      
            for MpiItem in listMpiOpts:
   
              if "-I" in MpiItem:
                if strMpiIncTmp == "":
                  strMpiIncTmp = MpiItem[2:]
                else:
                  strMpiIncTmp += " "
                  strMpiIncTmp += MpiItem[2:]

                #strMpiInc.replace("-I","")
                #strMpiInc = '"' + strMpiIncTmp + '"'
                strMpiInc =  strMpiIncTmp 
                print "MPI Include: ", strMpiInc

              if "-L" in MpiItem:
                #if strMpiLibsTmp == "":
                  #strMpiLibsTmp = MpiItem[2:]
                #else:
                  #print(" ".join(strMpiLibsTmp))
                  #strMpiLibsTmp += " "
                  #strMpiLibsTmp += MpiItem[2:]
                  #os.system("echo "+ strMpiLibsTmp +" | sed -e 's/#/ /g'")
                  #strMpiLibsTmp = os.popen("echo "+ strMpiLibsTmp +" | sed -e 's/#/ /g'").read()

                strMpiLibsTmp = MpiItem[2:]
                strMpiLibs = strMpiLibsTmp 
                print "MPI Libs path: ", strMpiLibs
  
              if "-l" in MpiItem:
                strMpiLibraryTmp = MpiItem 

                #strMpiLibrary = '"' + strMpiLibraryTmp + '"'
                strMpiLibrary = strMpiLibraryTmp
                print "MPI Library: ", strMpiLibrary

            #strMpiLibs = '"' + strMpiLibsTmp + '"'
            #strMpiLibs = strMpiLibsTmp 
            print "MPI Libs path: ", strMpiLibs
 
            options.append('-mpi')
            #options.append('-mpiinc=/packages/mpich2/3.1.4_gcc-4.9.2/include')
            options.append('-mpiinc='+strMpiInc)
            #options.append('-mpilib=/packages/mpich2/3.1.4_gcc-4.9.2/lib')
            options.append('-mpilib='+strMpiLibs)
            #options.append('-mpilibrary=-lmpi')
            #options.append('-mpilibrary='+strMpiLibrary)
            libintl=spec['gettext'].prefix+'/lib'
            options.append('-mpilibrary='+strMpiLibrary+' -L'+libintl+' -Wl,-rpath,'+libintl)

        if '+shmem' in spec:
            options.append('-shmem')

        if '+gasnet' in spec:
            options.append('-gasnet=%s' % spec['gasnet'].prefix)

        if '+cuda' in spec:
            options.append("-cuda=%s" % spec['cuda'].prefix)

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        if '+comm' in spec:
            options.append('-PROFILECOMMUNICATORS')

        
        #env['CC'] = spec['mpi'].mpicc
        #env['CXX'] = spec['mpi'].mpicxx
        #env['F77'] = spec['mpi'].mpif77
        #env['FC'] = spec['mpi'].mpifc

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
