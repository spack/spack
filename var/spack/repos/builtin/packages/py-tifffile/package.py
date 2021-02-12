# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTifffile(PythonPackage):
    """Read and write image data from and to TIFF files."""

    homepage = "https://github.com/blink1073/tifffile"
    pypi = "tifffile/tifffile-0.12.1.tar.gz"

    version('2021.2.1',   sha256='6793787742e18cf2116bc65e17c51cd9c14cd27a4a6033a8ddd5bf801a637615')
    version('2021.1.14',  sha256='a5f8caaf672dab0dc8b2609b61d4fd23c6b6fe7e9df38750d4c872962a080ba9')
    version('2021.1.11',  sha256='abd731e7493c320e641486e90557beb77cecbfc82bc6a0a236d41365c81c83ec')
    version('2021.1.8',   sha256='b26e0373eca968f672043814a880700677ca1f6d1ce8a4e4d22ec8aea2bc0fcb')
    version('2020.12.8',  sha256='6c65c3997a21cad40349921e557a383fd5f0ebd728f5e91fa6c8f8f9e45c4bbd')
    version('2020.12.4',  sha256='5a388f8f3ca3f69a62f7c1cda72837fa5e9070e89992e7702408a786d526b3ff')
    version('2020.11.26', sha256='c712df6f201385fbd3500e26e45dc20fabcbb0c6c1fbfb4c1e44538a9d0269a8')
    version('2020.11.18', sha256='bdc82db0c01c81bb8f74fd82f0dbd4ec01c5fd6a0be12755948a86c6bf82a5db')
    version('2020.10.1', sha256='799feeccc91965b69e1288c51a1d1118faec7f40b2eb89ad2979591b85324830')
    version('0.12.1', sha256='802367effe86b0d1e64cb5c2ed886771f677fa63260b945e51a27acccdc08fa1')

    depends_on('python@3.7:', type=('build', 'run'), when='@2020.10.1:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.8.2:', type=('build', 'run'))
    depends_on('py-numpy@1.15.1:', type=('build', 'run'), when='@2020.10.1:')
