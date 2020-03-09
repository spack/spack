# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMaestrowf(PythonPackage):
    """A general purpose workflow conductor for running multi-step
       simulation studies."""

    homepage = "https://github.com/LLNL/maestrowf/"
    url      = "https://github.com/LLNL/maestrowf/archive/v1.1.6.tar.gz"
    git      = "https://github.com/LLNL/maestrowf/"

    maintainers = ['FrankD412']

    # git branches
    version('develop', branch='develop')
    version('master',  branch='master')

    # Pre-release candidates
    version('1.1.5dev',    sha256='eb3d6f31c233e2cde3b84e15c657002b83ff43d4d6b218b33d023a4f527b9e08')
    version('1.1.4dev1.0', sha256='67f59eed6fa69fc71b88a0a769de9f080300497d3c30d3a0893eabd0702bc48e')
    version('1.1.4dev1.1', sha256='c8612b5423b44f11e2a7c4fbc31eb741013245870512ee2dbf7367024517528f')

    # pypi releases
    version('1.1.6', sha256='27a4ab9072c5b5e2edf91c192d9fe67f040dd45be7f3e44fd9a998ce4cb1e92d', preferred=True)
    version('1.1.4', sha256='2cb0fa6f6281d8618ac79217ea5f4fd8cb24955c4315e873657f96b815f171d5')
    version('1.1.2', sha256='ebb45bff54625435bc9f2462e1bdc3b5bdc4d943378c53e7810c11836794c5e0')
    version('1.1.1', sha256='a476ad4b40846d7b7f9540d6413df1b42eb655735e8d3c6c07e0baa68e20a8bb')
    version('1.1.0', sha256='14e701d6a10ab758215aab6b6809817d9a39416a4f477cd2f2551883fc68477b')
    version('1.0.1', sha256='cdd503f0b11db9114405132274b28766044402d1183b5836406ed91d558fd06c')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml@4.2b1:',     type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-enum34',     type=('build', 'run'), when='^python@:3.3')
    depends_on('py-enum34',     type=('build', 'run'), when='@:1.1.3')
    depends_on('py-tabulate',   type=('build', 'run'), when='@1.1.0:')
    depends_on('py-filelock',   type=('build', 'run'), when='@1.1.0:')
