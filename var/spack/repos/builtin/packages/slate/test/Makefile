# Assumes BLAS++ and LAPACK++ are installed in SLATE directory.
# Otherwise would need to add
#   -I${blaspp_dir}/include -I${lapackpp_dir}/include to CXXFLAGS,
#   -L${blaspp_dir}/lib -L${lapackpp_dir}/lib and corresponding rpaths to LDFLAGS.
#
# Assumes everything built as shared libraries, so transitive dependencies
# are handled implicitly. That is, linking with -lslate implicitly links with
# -lblaspp -llapackpp -lopenblas.
# Substitute your choice of BLAS/LAPACK library for -lopenblas.

-include make.inc

slate_dir ?= /opt/slate
scalapack_libs ?= -L/opt/scalapack/lib -lscalapack -lgfortran

# CXXFLAGS add /opt/slate/include to include path.
# LDFLAGS  add /opt/slate/lib     to lib path.
# Using -rpath avoids need to add ${slate_dir}/lib to $LD_LIBRARY_PATH.
CXX      = mpicxx
CXXFLAGS = -fopenmp -Wall -std=c++17 -MMD -I${slate_dir}/include
LDFLAGS  = -fopenmp -L${slate_dir}/lib -Wl,-rpath,${slate_dir}/lib
LIBS     =

# auto-detect OS
# $OSTYPE may not be exported from the shell, so echo it
ostype := $(shell echo $${OSTYPE})
ifneq ($(findstring darwin, $(ostype)),)
    # MacOS is darwin
    macos = 1
    LDD = otool -L
else
    LDD = ldd
endif


# ------------------------------------------------------------------------------
# Check if SLATE was compiled with cublas. If so, explicitly link cublas
# since it is called in the SLATE headers.
grep_cuda := ${shell ${LDD} ${slate_dir}/lib/libslate.so | grep cublas}
ifeq (${grep_cuda},)
    ${info SLATE without CUDA}
    CXXFLAGS += -DSLATE_NO_CUDA
else
    cuda_nvcc := ${shell which nvcc}
    CUDA_ROOT ?= $(cuda_nvcc:/bin/nvcc=)
    ${info SLATE with CUDA ${CUDA_ROOT}}
    ifeq (${cuda_nvcc},)
        ${error SLATE compiled with CUDA, but cannot find nvcc.}
    endif

    CXXFLAGS += -I${CUDA_ROOT}/include
    LDFLAGS  += -L${CUDA_ROOT}/lib -Wl,-rpath,${CUDA_ROOT}/lib
    LIBS     += -lcublas -lcudart
endif


# ------------------------------------------------------------------------------
# SLATE examples
# Link with -lslate.
# Implicitly links with -lblaspp -llapackpp -lopenblas.

slate_src = ${wildcard slate*.cc}
slate_exe = ${basename ${slate_src}}

${slate_exe}: %: %.o
	${CXX} -o $@ $^ \
		${LDFLAGS} \
		-lslate ${LIBS}


# ------------------------------------------------------------------------------
# ScaLAPACK examples
# Link with -lslate_scalapack_api -lscalapack.
# Implicitly links with -lslate -lblaspp -llapackpp -lopenblas.

scalapack_src = ${wildcard scalapack*.cc}
scalapack_exe = ${basename ${scalapack_src}}

${scalapack_exe}: %: %.o
	${CXX} -o $@ $^ \
		${LDFLAGS} \
		-lslate_scalapack_api ${LIBS} \
		${scalapack_libs}


# ------------------------------------------------------------------------------
# BLAS++ examples
# Link with -lblaspp.
# Implicitly links with -lopenblas.

blaspp_src = ${wildcard blas*.cc}
blaspp_exe = ${basename ${blaspp_src}}

${blaspp_exe}: %: %.o
	${CXX} -o $@ $^ \
		 ${LDFLAGS} \
		 -lblaspp ${LIBS}


# ------------------------------------------------------------------------------
# LAPACK++ examples
# Link with -llapackpp -lblaspp.
# Implicitly links with -lopenblas.

lapackpp_src = ${wildcard lapack*.cc}
lapackpp_exe = ${basename ${lapackpp_src}}

${lapackpp_exe}: %: %.o
	${CXX} -o $@ $^ \
		${LDFLAGS} \
		-llapackpp -lblaspp ${LIBS}


# ------------------------------------------------------------------------------
# Generic rules.

exe = ${slate_exe} ${scalapack_exe} ${blaspp_exe} ${lapackpp_exe}

all: ${exe}

.DEFAULT_GOAL := all
.SUFFIXES:

%.o: %.cc
	${CXX} ${CXXFLAGS} -c -o $@ $<

clean:
	-rm -f ${exe} *.o

clean_exe:
	-rm -f ${exe}

distclean: clean clean_run
	-rm -f *.d

-include *.d


# ------------------------------------------------------------------------------
# Run examples.

txt = ${addsuffix .txt,${exe}}
txt_no_mpi = blas00_gemm.txt blas01_util.txt lapack00_potrf.txt

run:
	${MAKE} -j1 run_not_parallel

run_not_parallel: ${txt}

${txt_no_mpi}: %.txt: %
	./$< > $@

%.txt: %
	mpirun -np 4 ./$< | sort -s -k 2n > $@

clean_run:
	-rm -f ${txt}

# ------------------------------------------------------------------------------
# Debugging

echo:
	@echo "CXX       = ${CXX}"
	@echo "CXXFLAGS  = ${CXXFLAGS}"
	@echo "LDFLAGS   = ${LDFLAGS}"
	@echo "LIBS      = ${LIBS}"
	@echo "LDD       = ${LDD}"
	@echo
	@echo "macos     = ${macos}"
	@echo "grep_cuda = ${grep_cuda}"
	@echo "cuda_nvcc = ${cuda_nvcc}"
	@echo "CUDA_ROOT = ${CUDA_ROOT}"
	@echo
	@echo "slate_dir = ${slate_dir}"
	@echo "scalapack_libs = ${scalapack_libs}"
	@echo
	@echo "slate_src = ${slate_src}"
	@echo "slate_exe = ${slate_exe}"
	@echo
	@echo "scalapack_src = ${scalapack_src}"
	@echo "scalapack_exe = ${scalapack_exe}"
	@echo
	@echo "blaspp_src = ${blaspp_src}"
	@echo "blaspp_exe = ${blaspp_exe}"
	@echo
	@echo "lapackpp_src = ${lapackpp_src}"
	@echo "lapackpp_exe = ${lapackpp_exe}"
	@echo
	@echo "exe = ${exe}"
	@echo
	@echo "txt = ${txt}"
