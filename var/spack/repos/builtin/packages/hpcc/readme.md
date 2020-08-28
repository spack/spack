
Command line examples for HPCC installation with Spack:

```bash
# Simple install
# most likely (GCC, OpenMPI, OpenBLAS and FFTE)
spack install hpcc


# Install with GCC, OpenMPI, OpenBLAS and FFTE (build in copy):
spack install --test=root hpcc%gcc^openmpi^openblas

# Install with GCC, OpenMPI, OpenBLAS and FFTW2:
spack install --test=root hpcc fft=fftw2 %gcc^openmpi^openblas


# Install with intel compiler, intel mkl, intel-mpi and FFTE (build in copy):
spack install --test=root hpcc%intel^intel-parallel-studio@cluster.2020.2+mpi+mkl

# Install with intel compiler, intel mkl, intel-mpi and intel mkl (for FFT):
spack install --test=root hpcc fft=mkl %intel^intel-parallel-studio@cluster.2020.2+mpi+mkl
spack install --test=root hpcc fft=mkl %intel@19.0.5.281^intel-mkl@2019.5.281^intel-mpi@2019.5.281

# Install with intel compiler, intel mkl, intel-mpi and FFTW2:
spack install --test=root hpcc fft=fftw2 %intel^intel-parallel-studio@cluster.2020.2+mpi+mkl

```