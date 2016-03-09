import os
from spack import *


class Petsc(Package):
    """
    PETSc is a suite of data structures and routines for the scalable (parallel) solution of scientific applications
    modeled by partial differential equations.
    """

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz"

    version('3.6.3', '91dd3522de5a5ef039ff8f50800db606')
    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f')
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13')
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f')
    version('3.4.4', '7edbc68aa6d8d6a3295dd5f6c2f6979d')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('double', default=True, description='Switches between single and double precision')

    variant('metis', default=True, description='Activates support for metis and parmetis')
    variant('hdf5', default=True, description='Activates support for HDF5 (only parallel)')
    variant('boost', default=True, description='Activates support for Boost')
    variant('hypre', default=True, description='Activates support for Hypre')

    # Virtual dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    # Build dependencies
    depends_on('python @2.6:2.7')

    # Other dependencies
    depends_on('boost', when='+boost')
    depends_on('metis', when='+metis')

    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('parmetis', when='+metis+mpi')
    depends_on('hypre',    when='+hypre+mpi')

    def mpi_dependent_options(self):
        if '~mpi' in self.spec:
            compiler_opts = [
                '--with-cc=%s' % os.environ['CC'],
                '--with-cxx=%s' % (os.environ['CXX'] if self.compiler.cxx is not None else '0'),
                '--with-fc=%s' % (os.environ['FC'] if self.compiler.fc is not None else '0'),
                '--with-mpi=0'
            ]
            error_message_fmt = '\t{library} support requires "+mpi" to be activated'

            # If mpi is disabled (~mpi), it's an error to have any of these enabled.
            # This generates a list of any such errors.
            errors = [error_message_fmt.format(library=x)
                      for x in ('hdf5', 'hypre', 'parmetis')
                      if ('+'+x) in self.spec]
            if errors:
                errors = ['incompatible variants given'] + errors
                raise RuntimeError('\n'.join(errors))
        else:
            compiler_opts = [
                '--with-mpi=1',
                '--with-mpi-dir=%s' % self.spec['mpi'].prefix,
            ]
        return compiler_opts

    def install(self, spec, prefix):
        options = []
        options.extend(self.mpi_dependent_options())
        options.extend([
            '--with-precision=%s' % ('double' if '+double' in spec else 'single'),
            '--with-shared-libraries=%s' % ('1' if '+shared' in spec else '0'),
            '--with-blas-lapack-dir=%s' % spec['lapack'].prefix
        ])
        # Activates library support if needed
        for library in ('metis', 'boost', 'hdf5', 'hypre', 'parmetis'):
            options.append(
                '--with-{library}={value}'.format(library=library, value=('1' if library in spec else '0'))
            )
            if library in spec:
                options.append(
                    '--with-{library}-dir={path}'.format(library=library, path=spec[library].prefix)
                )

        configure('--prefix=%s' % prefix, *options)

        # PETSc has its own way of doing parallel make.
        make('MAKE_NP=%s' % make_jobs, parallel=False)
        make("install")
