# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildFramework(PythonPackage):
    """The core of EasyBuild, a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    pypi = 'easybuild-framework/easybuild-framework-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.3.2', sha256='2dbae21c742a1ec57e461ad9689c0139b1bfc17d70838aeefbee7a964878c587')
    version('4.3.1', sha256='6f3b82c4fc1fa4a7273e4ffb4766393064bec564051151d21ba96ea17611508a')
    version('4.3.0', sha256='97c42d8f26ebc6fc43748442a9f0bbbc5316ae38b8320f7052695d9b77e101ab')
    version('4.2.2', sha256='5752a21e991844637547f9106563fdcd6a667b492d3c3a89cd4da6d99a63a85f')
    version('4.2.1', sha256='530b071f541debccbc4b5a8e885ba6524ce398b9a12ea663c1129d0efb6a4a31')
    version('4.2.0', sha256='e260ad9c921c10873b0e3b6b322a42e5732fbed905cb50f5d189a4f54f4ad327')
    version('4.1.2', sha256='132bd4f1be05134d52cc5bd11c518c8f9f556205a354173690093850b94346b0')
    version('4.1.1', sha256='fa518f56cb7b54975e31e501d3d361907b921d5faa6befc910ff2575cdbb7c05')
    version('4.1.0', sha256='336b1adc3ea410aabf900a07f6a55dcf316dc55658afc1d665d3565040be0641')
    version('4.0.1', sha256='97ff2786bf8c5014f9ac3f3080fde07c5a66129dfe4e6f349cbe372cac82bb89')
    version('4.0.0', sha256='f5c40345cc8b9b5750f53263ade6c9c3a8cd3dfab488d58f76ac61a8ca7c5a77')
    version('3.1.2', sha256='a03598478574e2982587796afdb792d78b598f4c09ebf4bec1a690c06470c00d')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))
    depends_on('py-setuptools', when='@:3', type=('build', 'run'))
    depends_on('py-vsc-base@2.5.4:', when='@2.9:3', type='run')
