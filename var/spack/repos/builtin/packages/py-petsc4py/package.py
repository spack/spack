# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package.
    """

    homepage = "https://gitlab.com/petsc/petsc4py"
    url      = "https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc4py-3.15.0.tar.gz"
    git      = "https://gitlab.com/petsc/petsc.git"

    maintainers = ['balay']

    version('main', branch='main')
    version('3.16.4', sha256='51ac59be9d741ede95c8e0e13b6062b6fb1bd1c975da26732ba059ee8c5bb7eb')
    version('3.16.3', sha256='10e730d50716e40de55b200ff53b461bc4f3fcc798ba89b74dfe6bdf63fa7b6e')
    version('3.16.2', sha256='906634497ae9c59f2c97e12b935954e5ba95df2e764290c24fff6751b7510b04')
    version('3.16.1', sha256='c218358217c436947f8fd61f247f73ac65fa29ea3489ad00bef5827b1436b95f')
    version('3.16.0', sha256='4044accfdc2c80994e80e4e286478d1ba9ac358512d1b74c42e1327eadb0d802')
    version('3.15.5', sha256='cdbc8a7485960c80565268ae851639f6c620663f245708263a349903dd07e5ae')
    version('3.15.4', sha256='f3e1ae8db824d7ac6994f6ae4e04fdd76381f060ca350fee2a85aac668125a8c')
    version('3.15.3', sha256='06e7a5de3509067d8625330b10c1ab200b36df1dfdc2e93922038784b2722f8e')
    version('3.15.2', sha256='d7ed1d79d88b35da563d25e733f276595ba538c52756225f79ba92e1cc4658d3')
    version('3.15.1', sha256='4ec8f42081e4d6a61157b32869b352dcb18c69077f2d1e4160f3837efd9e150f')
    version('3.15.0', sha256='87dcc5ef63a1f0e1a963619f7527e623f52341b2806056b0ef5fdfb0b8b287ad')
    version('3.14.1', sha256='f5f8daf3a4cd1dfc945876b0d83a05b25f3c54e08046312eaa3e3036b24139c0')
    version('3.14.0', sha256='33ac9fb55a541e4c1deabd6e2144da96d5ae70e70c830a55de558000cf3f0ec5')
    version('3.13.0', sha256='0e11679353c0c2938336a3c8d1a439b853e20d3bccd7d614ad1dbea3ec5cb31f')
    version('3.12.0', sha256='4c94a1dbbf244b249436b266ac5fa4e67080d205420805deab5ec162b979df8d')
    version('3.11.0', sha256='ec114b303aadaee032c248a02021e940e43c6437647af0322d95354e6f2c06ad')
    version('3.10.1', sha256='11b59693af0e2067f029924dd6b5220f7a7ec00089f6e2c2361332d6123ea6f7')
    version('3.10.0', sha256='4e58b9e7d4343adcf905751261b789c8c3489496f8de5c3fc3844664ef5ec5a3')
    version('3.9.1',  sha256='8b7f56e0904c57cca08d1c24a1d8151d1554f06c9c5a31b16fb6db3bc928bbd8')
    version('3.9.0',  sha256='ae077dffd455014de16b6ed4ba014ac9e10227dc6b93f919a4229e8e1c870aec')
    version('3.8.1',  sha256='f6260a52dab02247f5b8d686a0587441b1a2048dff52263f1db42e75d2e3f330')
    version('3.8.0',  sha256='3445da12becf23ade4d40cdd04c746581982ab6a27f55fbb5cd29bc5560df4b1')
    version('3.7.0',  sha256='c04931a5ba3fd7c8c8d165aa7908688921ce3cf4cf8725d0cba73380c2107386')

    variant('mpi', default=True,  description='Activates MPI support')

    patch('ldshared.patch', when='@:99')
    patch('ldshared-dev.patch', when='@main')

    depends_on('py-cython', type='build', when='@main')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    depends_on('petsc+mpi', when='+mpi')
    depends_on('petsc~mpi', when='~mpi')
    depends_on('petsc@main', when='@main')
    depends_on('petsc@3.16.0:3.16', when='@3.16.0:3.16')
    depends_on('petsc@3.15.0:3.15', when='@3.15.0:3.15')
    depends_on('petsc@3.14.2:3.14', when='@3.14.1:3.14')
    depends_on('petsc@3.14.0:3.14.1', when='@3.14.0')
    depends_on('petsc@3.13.0:3.13', when='@3.13.0:3.13')
    depends_on('petsc@3.12.0:3.12', when='@3.12.0:3.12')
    depends_on('petsc@3.11.0:3.11', when='@3.11.0:3.11')
    depends_on('petsc@3.10.3:3.10', when='@3.10.1:3.10')
    depends_on('petsc@3.10:3.10.2', when='@3.10.0')
    depends_on('petsc@3.9.0:3.9', when='@3.9.0:3.9')
    depends_on('petsc@3.8.0:3.8', when='@3.8.0:3.8')
    depends_on('petsc@3.7.0:3.7', when='@3.7.0:3.7')
    depends_on('petsc@3.6.0:3.6', when='@3.6.0:3.6')

    @property
    def build_directory(self):
        import os
        if self.spec.satisfies('@main'):
            return os.path.join(self.stage.source_path, 'src', 'binding', 'petsc4py')
        else:
            return self.stage.source_path
