#Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class PyMeshpy(PythonPackage):
    """
    Triangular and Tetrahedral Mesh Generator
    """

    homepage = "https://documen.tician.de/meshpy"
    url      = "https://pypi.io/packages/source/M/MeshPy/MeshPy-2020.1.tar.gz"
    git      ="https://github.com/inducer/meshpy.git"

    maintainers = ['samcom12','jayashripawar']

    version('main', branch='main')
    version('2020.1', sha256='7b14eef33ccfb7974c058cea04672bfcd66e57dfcfa6a65cf01943b08964e879')
    version('2018.2.1', sha256='4e6d18c2d19cda540967b6dc6ca844926020c9134cb4075c0f73d47fbbdb2f9e')
    version('2018.2', sha256='6685f59a09863f4d26b603e3f52454edaca72ba2bf4c553a21474faf2027426e')
    version('2018.1.1', sha256='dac617a242c9c183635fc16aedf5ce3772ef3509fd7c46e7175445448def6610')
    version('2018.1', sha256='aeacf8098939648e097f54ffa6351931f164e35166dc921d52346df6337d26fb')
    version('2016.1.2', sha256='43ff2f9b010183ed679632a6eaa3ff8fb7a2015024aee5cbb00ea49c821ac0b4')
    version('2016.1.1', sha256='5d4ee8867b9aa03c903e1aa7bdfabb47ae07c330376293c21082c27eeb2e7dc7')
    version('2016.1', sha256='a9e80c1f23f6a6cdc66f8f62ea63dc273664f357d25e572bc5edf5f9b22af7d9')
    version('2014.1', sha256='a090729c9b99360b2741099906361b2e9ba6373b97707817c9b81f66531380b6')
    version('2013.1.2', sha256='425ffa0f5a7dacfc1301bbb165ff78fbe6beacb0ab6c0a8dd581f565896c6762')
    version('2013.1.1', sha256='d89bf7e0af003784e3a7f35ea320a522b5a6dabc03530ad2bcbc93c6e575fa29')
    version('2013.1', sha256='e82e67ac8c8bbc79680d3c826b7f1e6624e4df7e170e1a669699a29c9a21a92e')
    version('2011.1', sha256='ecbda1c9ba7b2f770605cf611e5b069f330eeb9d85860dffc774f11861992e05')
    version('0.91.2', sha256='d971a99d6d7cae85b48718ab824dba4fab6fce9951ff1e4d07d366d1129c4274')
    version('0.91.1', sha256='08d8662a7703f0eb8934080f718f30c40aa0b3edd45fb3467512577f26b4c8d3')
    version('0.91', sha256='db11f994b6b321cadf4b41741fea284122385ec6ca4544b134ef2e34929d5afe')

    depends_on('python@3.6:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'run'))
    conflicts('%gcc@:4.7', msg='GCC 4.8+ required')
