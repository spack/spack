#!/bin/bash

# Script 1: 
           # set the variables that are the same across zlib/pigz & variables for zlib
           # the first amount of stuff that can run in parallel? 
echo "Script 1 starting..."
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src
export CMAKE_PREFIX_PATH=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gmake-4.4.1-h4caimdpmzjqeyrfqjwkkivkrij43g67:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx;
export PATH=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gmake-4.4.1-h4caimdpmzjqeyrfqjwkkivkrij43g67/bin:/dev/shm/shea9/spack/lib/spack/env/gcc:/dev/shm/shea9/spack/lib/spack/env/case-insensitive:/dev/shm/shea9/spack/lib/spack/env:/dev/shm/shea9/spack/bin:/usr/tce/packages/python/python-3.10.8/bin:/dev/shm/shea9/spack/bin:/usr/tce/packages/texlive/texlive-20220321/bin/x86_64-linux:/usr/tce/packages/texlive/texlive-20220321/bin:/usr/global/tools/jobutils/bin:/usr/tce/packages/mvapich2/mvapich2-2.3.7-intel-classic-2021.6.0-magic/bin:/usr/tce/packages/intel-classic/intel-classic-2021.6.0-magic/bin:/usr/tce/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:.;
export SPACK_CFLAGS=-fPIC;
export SPACK_DEBUG_LOG_DIR=/dev/shm/shea9;
export SPACK_DEBUG_LOG_ID=zlib-ng-nafn5km;
export SPACK_SHORT_SPEC="zlib-ng@2.1.6%gcc@10.3.1+compat+new_strategies+opt+pic+shared build_system=autotools arch=linux-rhel8-icelake/nafn5km";
export SPACK_STORE_INCLUDE_DIRS="";
export SPACK_STORE_LINK_DIRS=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx/lib;
export SPACK_STORE_RPATH_DIRS=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib64:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx/lib;
unset ZPOOL_SCRIPTS_AS_ROOT;
unset R_HOME;
unset R_ENVIRON;
unset PYTHONPATH;
unset OBJC_INCLUDE_PATH;
unset MPIFC;
unset MPIF90;
unset MPIF77;
unset MPICXX;
unset MPICC;
unset MODULEPATH_ROOT;
unset LUA_PATH;
unset LUA_CPATH;
unset LMOD_ROOT;
unset LIBS;
unset LIBRARY_PATH;
unset LD_RUN_PATH;
unset LD_PRELOAD;
unset LD_LIBRARY_PATH;
unset LDFLAGS;
unset FLIBS;
unset FFLAGS;
unset FCLIBS;
unset FCFLAGS;
unset DYLD_LIBRARY_PATH;
unset DYLD_INSERT_LIBRARIES;
unset DYLD_FALLBACK_LIBRARY_PATH;
unset CXXFLAGS;
unset CXXCPP;
unset CPPFLAGS;
unset CPP;
unset CPLUS_INCLUDE_PATH;
unset CPATH;
unset C_INCLUDE_PATH;
unset CFLAGS;
unset CCC;
export SPACK_TARGET_ARGS="-march=icelake-client -mtune=icelake-client";
export SPACK_SYSTEM_DIRS="\"/\"|\"//\"|\"/bin\"|\"/bin/\"|\"/bin64\"|\"/bin64/\"|\"/include\"|\"/include/\"|\"/lib\"|\"/lib/\"|\"/lib64\"|\"/lib64/\"|\"/usr\"|\"/usr/\"|\"/usr/bin\"|\"/usr/bin/\"|\"/usr/bin64\"|\"/usr/bin64/\"|\"/usr/include\"|\"/usr/include/\"|\"/usr/lib\"|\"/usr/lib/\"|\"/usr/lib64\"|\"/usr/lib64/\"|\"/usr/local\"|\"/usr/local/\"|\"/usr/local/bin\"|\"/usr/local/bin/\"|\"/usr/local/bin64\"|\"/usr/local/bin64/\"|\"/usr/local/include\"|\"/usr/local/include/\"|\"/usr/local/lib\"|\"/usr/local/lib/\"|\"/usr/local/lib64\"|\"/usr/local/lib64/\"";
export SPACK_RPATH_DIRS="";
export SPACK_MANAGED_DIRS="\"/dev/shm/shea9/spack/opt/spack/\"*|\"/dev/shm/shea9/tmp/spack-stage/\"*";
export SPACK_LINKER_ARG=-Wl,;
export SPACK_LINK_DIRS="";
export SPACK_INCLUDE_DIRS="";
export SPACK_FC=/usr/tce/bin/gfortran;
export SPACK_FC_RPATH_ARG=-Wl,-rpath,;
export SPACK_F77=/usr/tce/bin/gfortran;
export SPACK_F77_RPATH_ARG=-Wl,-rpath,;
export SPACK_ENV_PATH=/dev/shm/shea9/spack/lib/spack/env:/dev/shm/shea9/spack/lib/spack/env/case-insensitive:/dev/shm/shea9/spack/lib/spack/env/gcc;
export SPACK_DTAGS_TO_STRIP=--enable-new-dtags;
export SPACK_DTAGS_TO_ADD=--disable-new-dtags;
export SPACK_DEBUG=TRUE;
export SPACK_CXX=/usr/tce/bin/g++;
export SPACK_CXX_RPATH_ARG=-Wl,-rpath,;
export SPACK_COMPILER_SPEC=gcc@=10.3.1;
export SPACK_COMPILER_IMPLICIT_RPATHS=/collab/usr/global/tools/tce4/packages/gcc/gcc-10.3.1/lib/gcc/x86_64-redhat-linux/10;
export SPACK_COMPILER_FLAGS_REPLACE="-Werror-|-Wno-error= -Werror|-Wno-error";
export SPACK_CC=/usr/tce/bin/gcc;
export SPACK_CC_RPATH_ARG=-Wl,-rpath,;
export LC_ALL=C;
export FC=/dev/shm/shea9/spack/lib/spack/env/gcc/gfortran;
export F77=/dev/shm/shea9/spack/lib/spack/env/gcc/gfortran;
export CXX=/dev/shm/shea9/spack/lib/spack/env/gcc/g++;
export CC=/dev/shm/shea9/spack/lib/spack/env/gcc/gcc;
echo "Script 1 done."
