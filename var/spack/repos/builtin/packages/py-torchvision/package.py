# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorchvision(PythonPackage):
    """The torchvision package consists of popular datasets, model
    architectures, and common image transformations for computer vision."""

    homepage = "https://github.com/pytorch/vision"
    url      = "https://github.com/pytorch/vision/archive/v0.7.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'torchvision', 'torchvision.datasets', 'torchvision.models',
        'torchvision.transforms', 'torchvision.ops',
        'torchvision.models.segmentation',
        'torchvision.models.detection'
    ]

    version('0.7.0', sha256='fa0a6f44a50451115d1499b3f2aa597e0092a07afce1068750260fa7dd2c85cb')
    version('0.6.1', sha256='8173680a976c833640ecbd0d7e6f0a11047bf8833433e2147180efc905e48656')
    version('0.6.0', sha256='02de11b3abe6882de4032ce86dab9c7794cbc84369b44d04e667486580f0f1f7')
    version('0.5.0', sha256='eb9afc93df3d174d975ee0914057a9522f5272310b4d56c150b955c287a4d74d')
    version('0.4.2', sha256='1184a27eab85c9e784bacc6f9d6fec99e168ab4eda6047ef9f709e7fdb22d8f9')
    version('0.4.1', sha256='053689351272b3bd2ac3e6ba51efd284de0e4ca4a301f54674b949f1e62b7176')
    version('0.4.0', sha256='c270d74e568bad4559fed4544f6dd1e22e2eb1c60b088e04a5bd5787c4150589')
    version('0.3.0', sha256='c205f0618c268c6ed2f8abb869ef6eb83e5339c1336c243ad321a2f2a85195f0')

    # See README.rst
    depends_on('python@3.6:', when='@0.7:', type=('build', 'run'))
    depends_on('python@3.5:', when='@0.6.0:0.6.999', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:3.8', when='@0.5.0', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:3.7', when='@:0.4', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('ninja', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', when='@:0.5', type=('build', 'run'))

    # See README.rst
    depends_on('py-torch@1.6.0', when='@0.7.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.5.1', when='@0.6.1', type=('build', 'link', 'run'))
    depends_on('py-torch@1.5.0', when='@0.6.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.4.0', when='@0.5.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.3.1', when='@0.4.2', type=('build', 'link', 'run'))
    depends_on('py-torch@1.3.0', when='@0.4.1', type=('build', 'link', 'run'))
    depends_on('py-torch@1.2.0', when='@0.4.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.1.0', when='@0.3.0', type=('build', 'link', 'run'))
    depends_on('py-torch@:1.0.1', when='@0.2.2', type=('build', 'link', 'run'))

    # TODO: Torchvision supports the following backends:
    # * pillow
    # * pillow-simd
    # * accimage
    # * libpng
    # * libjpeg

    # https://github.com/pytorch/vision/issues/1712
    depends_on('py-pillow@4.1.1:6', when='@:0.4', type=('build', 'run'))
    depends_on('py-pillow@4.1.1:',  when='@0.5:', type=('build', 'run'))

    # Many of the datasets require additional dependencies to use.
    # These can be installed after the fact.
    depends_on('py-scipy', type='test')

    depends_on('ffmpeg@3.1:', when='@0.4.2:')

    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)
            library.extend(query.libs.directories)

        # README says to use TORCHVISION_INCLUDE and TORCHVISION_LIBRARY,
        # but these do not work. Build uses a mix of Spack's compiler wrapper
        # and the actual compiler, so this is needed to get parts of the build
        # working. See https://github.com/pytorch/vision/issues/2591
        env.set('CPATH', ':'.join(include))
        env.set('LIBRARY_PATH', ':'.join(library))

        if '+cuda' in self.spec['py-torch']:
            env.set('FORCE_CUDA', 1)
        else:
            env.set('FORCE_CUDA', 0)
