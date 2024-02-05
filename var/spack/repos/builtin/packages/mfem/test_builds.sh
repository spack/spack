#!/bin/bash

dry_run=yes

# use 'dev-build' in "$mfem_src_dir":
spack_dev_build=no
mfem_src_dir=$HOME/mfem-spack

# Set a compiler to test with, e.g. '%gcc', '%clang', etc.
compiler=''
cuda_arch="70"
rocm_arch="gfx908"

spack_jobs=''
# spack_jobs='-j 128'

mfem='mfem@4.6.0'${compiler}
# mfem_dev='mfem@develop'${compiler}
mfem_dev='mfem@4.6.0'${compiler}

backends='+occa+raja+libceed'
backends_specs='^occa~cuda ^raja~openmp'

# ~fortran is needed for Cray Fortran linking with tcmalloc*
conduit_spec='^conduit~fortran'
# petsc spec
petsc_spec='^petsc+mumps'
petsc_spec_cuda='^petsc+cuda+mumps'
petsc_spec_rocm='^petsc+rocm+mumps'
# strumpack spec without cuda (use version > 6.3.1)
strumpack_spec='^strumpack~slate~openmp~cuda'
strumpack_cuda_spec='^strumpack+cuda~slate~openmp'
strumpack_rocm_spec='^strumpack+rocm~slate~openmp~cuda'
# superlu specs with cuda and rocm
superlu_cuda_spec='^superlu-dist+cuda'
superlu_rocm_spec='^superlu-dist+rocm'

builds=(
    # preferred version:
    ${mfem}
    ${mfem}'~mpi~metis~zlib'
    ${mfem}"$backends"'+superlu-dist+strumpack+suite-sparse+petsc+slepc+gslib \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        '"$backends_specs $strumpack_spec $petsc_spec $conduit_spec"
    ${mfem}'~mpi \
        '"$backends"'+suite-sparse+sundials+gslib+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        '"$backends_specs $conduit_spec"' ^sundials~mpi'

    # develop version, shared builds:
    ${mfem_dev}'+shared~static'
    ${mfem_dev}'+shared~static~mpi~metis~zlib'
    # NOTE: Shared build with +gslib works on mac but not on linux
    # TODO: add back '+gslib' when the above NOTE is addressed.
    ${mfem_dev}'+shared~static \
        '"$backends"'+superlu-dist+strumpack+suite-sparse+petsc+slepc \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        '"$backends_specs $strumpack_spec $petsc_spec $conduit_spec"
    # NOTE: Shared build with +gslib works on mac but not on linux
    # TODO: add back '+gslib' when the above NOTE is addressed.
    ${mfem_dev}'+shared~static~mpi \
        '"$backends"'+suite-sparse+sundials+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        '"$backends_specs $conduit_spec"' ^sundials~mpi'
)

builds2=(
    # preferred version
    ${mfem}"$backends $backends_specs"
    ${mfem}'+superlu-dist'
    ${mfem}'+strumpack'" $strumpack_spec"
    ${mfem}'+suite-sparse~mpi'
    ${mfem}'+suite-sparse'
    ${mfem}'+sundials~mpi ^sundials~mpi'
    ${mfem}'+sundials'
    ${mfem}'+pumi'
    ${mfem}'+gslib'
    ${mfem}'+netcdf~mpi'
    ${mfem}'+netcdf'
    ${mfem}'+mpfr'
    ${mfem}'+gnutls'
    ${mfem}'+conduit~mpi'" $conduit_spec"
    ${mfem}'+conduit'" $conduit_spec"
    ${mfem}'+umpire'
    ${mfem}'+petsc'" $petsc_spec"
    ${mfem}'+petsc+slepc'" $petsc_spec"
    ${mfem}'+ginkgo'
    ${mfem}'+hiop'
    ${mfem}'+threadsafe'
    # hypre+int64 requires 64-bit blas+lapack
    # ${mfem}' ^hypre+int64'
    ${mfem}' ^hypre+mixedint'
    #
    # develop version
    ${mfem_dev}"$backends $backends_specs"
    ${mfem_dev}'+superlu-dist'
    ${mfem_dev}'+strumpack'" $strumpack_spec"
    ${mfem_dev}'+suite-sparse~mpi'
    ${mfem_dev}'+suite-sparse'
    ${mfem_dev}'+sundials~mpi ^sundials~mpi'
    ${mfem_dev}'+sundials'
    ${mfem_dev}'+pumi'
    ${mfem_dev}'+gslib'
    ${mfem_dev}'+netcdf~mpi'
    ${mfem_dev}'+netcdf'
    ${mfem_dev}'+mpfr'
    ${mfem_dev}'+gnutls'
    ${mfem_dev}'+conduit~mpi'" $conduit_spec"
    ${mfem_dev}'+conduit'" $conduit_spec"
    ${mfem_dev}'+umpire'
    ${mfem_dev}'+petsc'" $petsc_spec"
    ${mfem_dev}'+petsc+slepc'" $petsc_spec"
    ${mfem_dev}'+ginkgo'
    ${mfem_dev}'+hiop'
    ${mfem_dev}'+threadsafe'
    # hypre+int64 requires 64-bit blas+lapack
    # ${mfem_dev}' ^hypre+int64'
    ${mfem_dev}' ^hypre+mixedint'
)


builds_cuda=(
    # hypre without cuda:
    ${mfem}'+cuda cuda_arch='"${cuda_arch}"

    # hypre with cuda:
    ${mfem}'+cuda cuda_arch='"${cuda_arch} ^hypre+cuda"

    # hypre with cuda:
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    ${mfem}'+cuda+raja+occa cuda_arch='"${cuda_arch}"' \
        ^raja+cuda~openmp ^hypre+cuda'

    # hypre without cuda:
    # NOTE: PETSc tests may need PETSC_OPTIONS="-use_gpu_aware_mpi 0"
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    # TODO: remove "^hiop+shared" when the default static build is fixed.
    ${mfem}'+cuda+openmp+raja+occa cuda_arch='"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib+petsc+slepc \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        ^raja+cuda+openmp ^hiop+shared'" $strumpack_cuda_spec"' \
        '"$superlu_cuda_spec $petsc_spec_cuda $conduit_spec"

    # hypre with cuda:
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    # TODO: add back "+petsc+slepc $petsc_spec_cuda" when it works.
    # NOTE: PETSc tests may need PETSC_OPTIONS="-use_gpu_aware_mpi 0"
    # TODO: add back "+sundials" when it's supported with '^hypre+cuda'.
    # TODO: remove "^hiop+shared" when the default static build is fixed.
    ${mfem}'+cuda+openmp+raja+occa cuda_arch='"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib \
        +pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        ^raja+cuda+openmp ^hiop+shared ^hypre+cuda \
        '" $strumpack_cuda_spec $superlu_cuda_spec $conduit_spec"

    #
    # same builds as above with ${mfem_dev}
    #

    # hypre without cuda:
    ${mfem_dev}'+cuda cuda_arch='"${cuda_arch}"

    # hypre with cuda:
    ${mfem_dev}'+cuda cuda_arch='"${cuda_arch} ^hypre+cuda"

    # hypre with cuda:
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    ${mfem_dev}'+cuda+raja+occa cuda_arch='"${cuda_arch}"' \
        ^raja+cuda~openmp ^hypre+cuda'

    # hypre without cuda:
    # NOTE: PETSc tests may need PETSC_OPTIONS="-use_gpu_aware_mpi 0"
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    # TODO: remove "^hiop+shared" when the default static build is fixed.
    ${mfem_dev}'+cuda+openmp+raja+occa cuda_arch='"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib+petsc+slepc \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        ^raja+cuda+openmp ^hiop+shared'" $strumpack_cuda_spec"' \
        '"$superlu_cuda_spec $petsc_spec_cuda $conduit_spec"

    # hypre with cuda:
    # TODO: restore '+libceed' when the libCEED CUDA unit tests take less time.
    # TODO: add back "+petsc+slepc $petsc_spec_cuda" when it works.
    # NOTE: PETSc tests may need PETSC_OPTIONS="-use_gpu_aware_mpi 0"
    # TODO: add back "+sundials" when it's supported with '^hypre+cuda'.
    # TODO: remove "^hiop+shared" when the default static build is fixed.
    ${mfem_dev}'+cuda+openmp+raja+occa cuda_arch='"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib \
        +pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit+ginkgo+hiop \
        ^raja+cuda+openmp ^hiop+shared ^hypre+cuda \
        '"$strumpack_cuda_spec $superlu_cuda_spec $conduit_spec"
)


builds_rocm=(
    # hypre without rocm:
    ${mfem}'+rocm amdgpu_target='"${rocm_arch}"

    # hypre with rocm:
    ${mfem}'+rocm amdgpu_target='"${rocm_arch} ^hypre+rocm"

    # hypre with rocm:
    ${mfem}'+rocm+raja+occa+libceed amdgpu_target='"${rocm_arch}"' \
        ^raja+rocm~openmp ^occa~cuda~openmp ^hypre+rocm'

    # hypre without rocm:
    # TODO: add back '+hiop' when it is no longer linked with tcmalloc* through
    #       its magma dependency.
    # TODO: add back '+ginkgo' when the Ginkgo example works.
    ${mfem}'+rocm+openmp+raja+occa+libceed amdgpu_target='"${rocm_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib+petsc+slepc \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        ^raja+rocm~openmp ^occa~cuda'" $strumpack_rocm_spec"' \
        '"$superlu_rocm_spec $petsc_spec_rocm $conduit_spec"

    # hypre with rocm:
    # TODO: add back "+petsc+slepc $petsc_spec_rocm" when it works.
    # TODO: add back '+hiop' when it is no longer linked with tcmalloc* through
    #       its magma dependency.
    # TODO: add back '+ginkgo' when the Ginkgo example works.
    # TODO: add back "+sundials" when it's supported with '^hypre+rocm'.
    ${mfem}'+rocm+openmp+raja+occa+libceed amdgpu_target='"${rocm_arch}"' \
        +superlu-dist+strumpack+suite-sparse+gslib \
        +pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        ^raja+rocm~openmp ^occa~cuda ^hypre+rocm \
        '"$strumpack_rocm_spec $superlu_rocm_spec $conduit_spec"

    #
    # same builds as above with ${mfem_dev}
    #

    # TODO
)


trap 'printf "\nScript interrupted.\n"; exit 33' INT

SEP='=========================================================================='
sep='--------------------------------------------------------------------------'

run_builds=("${builds[@]}" "${builds2[@]}")
# run_builds=("${builds_cuda[@]}")
# run_builds=("${builds_rocm[@]}")

# PETSc CUDA tests on Lassen need this:
# export PETSC_OPTIONS="-use_gpu_aware_mpi 0"

# spack files to clean in "$mfem_src_dir" when using 'dev-build'
clean_files=(
    .spack_no_patches
    install-time-test-log.txt
    spack-build-\*.txt
)
if [[ "$spack_dev_build" != "yes" ]]; then
    spack_action=(install)
else
    spack_action=(dev-build -q -d "$mfem_src_dir")
fi
TIMEFORMAT=$'real: %3Rs (%lR)  user: %3Us  sys: %3Ss  %%cpu: %P'

# main loop over specs:
for bld in "${run_builds[@]}"; do
    eval bbb="\"${bld}\""

    printf "\n%s\n" "${SEP}"
    printf "    %s\n" "${bld}"
    printf "%s\n" "${SEP}"

    if [[ "$dry_run" != "yes" ]]; then

        if [[ "$spack_dev_build" == "yes" ]]; then
            echo "Cleaning $mfem_src_dir ..."
            (cd "$mfem_src_dir" && make distclean && rm -f ${clean_files[@]})
            printf "%s\n" "${sep}"
        fi
        time ./bin/spack spec --fresh -I $bbb || exit 1
        printf "%s\n" "${sep}"
        time ./bin/spack "${spack_action[@]}" $spack_jobs \
            --fresh --test=root $bbb || exit 2

    else # dry run

        if [[ "$spack_dev_build" == "yes" ]]; then
            printf '(cd "'"$mfem_src_dir"'" && make distclean && rm -f'
            printf " %s)\n" "${clean_files[*]}"
        fi
        echo time ./bin/spack spec --fresh -I $bbb
        echo time ./bin/spack "${spack_action[@]}" $spack_jobs \
            --fresh --test=root $bbb
        echo

    fi
done

# Uninstall all mfem builds:
# spack uninstall --all mfem
