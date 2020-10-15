from spack import *


class SpackDummyPackage(MakefilePackage):
    """An mpi hello world that is packaged for spack."""

    homepage = "http://www.anl.gov"
    git      = "https://github.com/frankwillmore/spack-dummy-package.git"

    version('master', branch='master')

    depends_on('mpi')

    def edit(self, spec, prefix):
        env['PREFIX'] = prefix
        print("running edit()")

    @when('^openmpi') 
    def edit(self, spec, prefix):
        env['CC'] = 'mpicc'
        env['MPIRUN'] = 'mpirun'
        print("using openmpi, setting CC=mpicc")

    def build(self, spec, prefix):
        make()
        make('check')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('mpi_hello', join_path(prefix.bin, 'mpi_hello'))

