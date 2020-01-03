# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path


class SpectrumMpi(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www-03.ibm.com/systems/spectrum-computing/products/mpi"

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('IBM MPI is not installable; it is vendor supplied')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.bin)
        env.prepend_path('MANPATH', os.path.join(self.prefix, 'share', 'man'))
        env.prepend_path('LD_RUN_PATH', self.prefix.lib)
        env.prepend_path(
            'PKG_CONFIG_PATH', os.path.join(self.prefix, 'lib', 'pkgconfig'))

        for path in ['LIBRARY_PATH', 'LD_LIBRARY_PATH']:
            env.prepend_path(path, self.prefix.lib)
            env.prepend_path(
                path, os.path.join(self.prefix, 'lib', 'pami_port'))

        env.prepend_path('LDFLAGS','-Wl,-rpath=' + self.prefix.lib)
        env.prepend_path('OMPI_LDFLAGS', '-Wl,-rpath='+ self.prefix.lib)
        env.prepend_path('OMPI_LDFLAGS', '-L' + self.prefix.lib)
        env.prepend_path('OMPI_CPPFLAGS', '-I' + self.prefix.include)
        env.prepend_path('OMPI_FCFLAGS', '-I{0} -I{1}'.format(
            self.prefix.include, self.prefix.lib))


    def setup_dependent_package(self, module, dependent_spec):
        # get the compiler names
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            self.spec.mpicc = os.path.join(self.prefix.bin, 'mpixlc')
            self.spec.mpicxx = os.path.join(self.prefix.bin, 'mpixlC')
            self.spec.mpif77 = os.path.join(self.prefix.bin, 'mpixlf')
            self.spec.mpifc = os.path.join(self.prefix.bin, 'mpixlf')
        elif '%pgi' in dependent_spec:
            self.spec.mpicc = os.path.join(self.prefix.bin, 'mpipgicc')
            self.spec.mpicxx = os.path.join(self.prefix.bin, 'mpipgic++')
            self.spec.mpif77 = os.path.join(self.prefix.bin, 'mpipgifort')
            self.spec.mpifc = os.path.join(self.prefix.bin, 'mpipgifort')
        else:
            self.spec.mpicc = os.path.join(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = os.path.join(self.prefix.bin, 'mpicxx')
            self.spec.mpif77 = os.path.join(self.prefix.bin, 'mpif77')
            self.spec.mpifc = os.path.join(self.prefix.bin, 'mpif90')

    def setup_dependent_build_environment(self, env, dependent_spec):
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            env.set('MPICC', os.path.join(self.prefix.bin, 'mpixlc'))
            env.set('MPICXX', os.path.join(self.prefix.bin, 'mpixlC'))
            env.set('MPIF77', os.path.join(self.prefix.bin, 'mpixlf'))
            env.set('MPIF90', os.path.join(self.prefix.bin, 'mpixlf'))
        elif '%pgi' in dependent_spec:
            env.set('MPICC', os.path.join(self.prefix.bin, 'mpipgicc'))
            env.set('MPICXX', os.path.join(self.prefix.bin, 'mpipgic++'))
            env.set('MPIF77', os.path.join(self.prefix.bin, 'mpipgifort'))
            env.set('MPIF90', os.path.join(self.prefix.bin, 'mpipgifort'))
        else:
            env.set('MPICC', os.path.join(self.prefix.bin, 'mpicc'))
            env.set('MPICXX', os.path.join(self.prefix.bin, 'mpic++'))
            env.set('MPIF77', os.path.join(self.prefix.bin, 'mpif77'))
            env.set('MPIF90', os.path.join(self.prefix.bin, 'mpif90'))

        env.set('OMPI_CC', spack_cc)
        env.set('OMPI_CXX', spack_cxx)
        env.set('OMPI_FC', spack_fc)
        env.set('OMPI_F77', spack_f77)

        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
