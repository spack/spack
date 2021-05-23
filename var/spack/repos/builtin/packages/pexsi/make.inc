# Different compiling and linking options.
SUFFIX = linux

# Compiler and tools
################################################################
CC = @MPICC
CXX = @MPICXX
FC = @MPIFC
LOADER = @MPICXX


AR = ar
ARFLAGS = rvcu
# For System V based machine without ranlib, like Cray and SGI,
# use touch instead.
RANLIB = @RANLIB

CP = cp
RM = rm
RMFLAGS = -f
################################################################

# PEXSI directory
PEXSI_DIR = @PEXSI_STAGE

# Required libraries directories
DSUPERLU_DIR = @SUPERLU_PREFIX
METIS_DIR = @METIS_PREFIX
PARMETIS_DIR = @PARMETIS_PREFIX
LAPACK_DIR = @LAPACK_PREFIX
BLAS_DIR = @BLAS_PREFIX

# Includes
PEXSI_INCLUDE = -I${PEXSI_DIR}/include
DSUPERLU_INCLUDE = -I${DSUPERLU_DIR}/include
INCLUDES = ${PEXSI_INCLUDE} ${DSUPERLU_INCLUDE}

# Libraries
CPP_LIB = @MPICXX_LIB @STDCXX_LIB
#GFORTRAN_LIB = /usr/lib/gcc/x86_64-linux-gnu/4.8/libgfortran.a
LAPACK_LIB = @LAPACK_LIBS
BLAS_LIB = @BLAS_LIBS
DSUPERLU_LIB = ${DSUPERLU_DIR}/lib/libsuperlu_dist.a
PEXSI_LIB = ${PEXSI_DIR}/src/libpexsi_${SUFFIX}.a

# Graph partitioning libraries
METIS_LIB = -L${METIS_DIR}/lib -lmetis
PARMETIS_LIB = -L${PARMETIS_DIR}/libparmetis -lparmetis

# Different compiling and linking options.
COMPILE_DEF = -DDEBUG=0 -DRELEASE
COMPILE_FLAG = -O3 -w

LIBS  = ${PEXSI_LIB} ${DSUPERLU_LIB} ${PARMETIS_LIB} ${METIS_LIB} ${LAPACK_LIB} ${BLAS_LIB} ${GFORTRAN_LIB}

COMPILE_DEF  += -DAdd_

CPPFLAG = -std=c++11

CFLAGS       = ${COMPILE_FLAG} ${PROFILE_FLAG} ${INCLUDES}
FFLAGS       = ${COMPILE_FLAG} ${PROFILE_FLAG} ${INCLUDES}
CXXFLAGS     = ${COMPILE_FLAG} ${CPPFLAG} ${PROFILE_FLAG} ${INCLUDES}
CCDEFS       = ${COMPILE_DEF}
CPPDEFS      = ${COMPILE_DEF}
LOADOPTS     = ${PROFILE_FLAG} ${LIBS}
FLOADOPTS    = @FLDFLAGS ${PROFILE_FLAG} ${LIBS} ${CPP_LIB}

# Generate auto-dependencies
%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CCDEFS) $(CFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@;\
	rm -f $@.$$$$

%.d: %.cpp
	@set -e; rm -f $@; \
	$(CXX) -M $(CPPDEFS) $(CXXFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@;\
	rm -f $@.$$$$
