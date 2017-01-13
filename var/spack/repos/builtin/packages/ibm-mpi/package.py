from spack import *

class IbmMpi(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/ibm-mpi-10.1.0.2.tar.gz"

    version('10.1.0.2', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('IBM MPI is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dspec):
        # get library name and directory
        spec = self.spec
        spec.mpi_base_dir = '/opt/ibm/spectrum_mpi'
        spec.mpi_library = '/opt/ibm/spectrum_mpi/lib/libmpi_ibm.so'
        spec.mpi_include_path = '/opt/ibm/spectrum_mpi/include'
        spec.mpi_exec = '/opt/ibm/spectrum_mpi/bin/mpirun'
        spec.mpi_np_flag = '-np'
        if '%xl' in dspec or '%xl_r' in dspec:
            spec.mpicc = '/opt/ibm/spectrum_mpi/bin/mpixlc'
            spec.mpicxx = '/opt/ibm/spectrum_mpi/bin/mpixlC'
            spec.mpif77 = '/opt/ibm/spectrum_mpi/bin/mpixlf'
            spec.mpif90 = '/opt/ibm/spectrum_mpi/bin/mpixlf'
            spec.mpifc = '/opt/ibm/spectrum_mpi/bin/mpixlf'
        else:
            spec.mpicc = '/opt/ibm/spectrum_mpi/bin/mpicc'
            spec.mpicxx = '/opt/ibm/spectrum_mpi/bin/mpicxx'
            spec.mpif77 = '/opt/ibm/spectrum_mpi/bin/mpif77'
            spec.mpif90 = '/opt/ibm/spectrum_mpi/bin/mpif90'
            spec.mpifc = '/opt/ibm/spectrum_mpi/bin/mpif90'
