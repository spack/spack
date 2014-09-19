import os
from spack import *

class Mvapich2(Package):
    """mvapich2 is an MPI implmenetation for infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"

    version('1.9', '5dc58ed08fd3142c260b70fe297e127c',
            url="http://mvapich.cse.ohio-state.edu/download/mvapich2/mv2/mvapich2-1.9.tgz")
    patch('ad_lustre_rwcontig_open_source.patch', when='@1.9')

    version('2.0', '9fbb68a4111a8b6338e476dc657388b4',
            url='http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.0.tar.gz')

    provides('mpi@:2.2', when='@1.9')    # MVAPICH2-1.9 supports MPI 2.2
    provides('mpi@:3.0', when='@2.0')    # MVAPICH2-2.0 supports MPI 3.0


    def install(self, spec, prefix):
        # we'll set different configure flags depending on our environment
        configure_args = []

        # TODO: The MPICH*_FLAGS have a different name for 1.9

        if '+debug' in spec:
            # set configure flags for debug build
            configure_args.append("--disable-fast")
            configure_args.append("--enable-g=dbg")
            configure_args.append("--enable-error-checking=runtime")
            configure_args.append("--enable-error-messages=all")
            configure_args.append("--enable-nmpi-as-mpi")

            if "%gnu" in spec:
                # set variables for GNU compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O0"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O0"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O0 -fno-second-underscore"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O0 -fno-second-underscore"
            elif "%intel" in spec:
                # set variables for Inel compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O0"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O0"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O0"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O0"
            elif "%pgi" in spec:
                # set variables for PGI compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O0 -fPIC"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O0 -fPIC"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O0 -fPIC"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O0 -fPIC"

        else:
            # set configure flags for normal optimizations
            configure_args.append("--enable-fast=all")
            configure_args.append("--enable-g=dbg")
            configure_args.append("--enable-nmpi-as-mpi")

            if "%gnu" in spec:
                # set variables for what compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O2"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O2"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O2 -fno-second-underscore"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O2 -fno-second-underscore"
            elif "%intel" in spec:
                # set variables for Inel compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O2"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O2"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O2"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O2"
            elif "%pgi" in spec:
                # set variables for PGI compilers
                os.environ['MPICHLIB_CFLAGS']   = "-g -O2 -fPIC"
                os.environ['MPICHLIB_CXXFLAGS'] = "-g -O2 -fPIC"
                os.environ['MPICHLIB_FFLAGS']   = "-g -O2 -fPIC"
                os.environ['MPICHLIB_F90FLAGS'] = "-g -O2 -fPIC"

        # determine network type by variant
        if "+psm" in spec:
            # throw this flag on QLogic systems to use PSM
            configure_args.append("--with-device=ch3:psm")
        else:
            # throw this flag on IB systems
            configure_args.append("--with-device=ch3:mrail", "--with-rdma=gen2")

        # TODO: shared-memory build

        # TODO: CUDA

        # TODO: other file systems like panasis

        configure(
            "--prefix=" + prefix,
            "--enable-f77", "--enable-fc", "--enable-cxx",
            "--enable-shared", "--enable-sharedlibs=gcc",
            "--enable-debuginfo",
            "--with-pm=no", "--with-pmi=slurm",
            "--enable-romio", "--with-file-system=lustre+nfs+ufs",
            "--disable-mpe", "--without-mpe",
            "--disable-silent-rules",
            *configure_args)

        make()

        make("install")
