# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleCloudCore(PythonPackage):
    """Google Cloud API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    pypi = "google-cloud-core/google-cloud-core-1.0.3.tar.gz"

    version('1.6.0', sha256='c6abb18527545379fc82efc4de75ce9a3772ccad2fc645adace593ba097cbb02')
    version('1.5.0', sha256='1277a015f8eeb014c48f2ec094ed5368358318f1146cf49e8de389962dc19106')
    version('1.4.4', sha256='5bf32a3476412bbbf37660d73c46a7217a0db7913d4f4db6490b56d7a93f1d86')
    version('1.4.3', sha256='21afb70c1b0bce8eeb8abb5dca63c5fd37fc8aea18f4b6d60e803bd3d27e6b80')
    version('1.4.2', sha256='a65d6485a8bc8d11ccb97d72a48213fa5d22012fb8779ef9f9d0dc1655fbd4fa')
    version('1.4.1', sha256='613e56f164b6bee487dd34f606083a0130f66f42f7b10f99730afdf1630df507')
    version('1.4.0', sha256='07a024a26c4eb14ee3df7e6e5021c04f8f7e9f0e83d3d47863229f3635f871ce')
    version('1.3.0', sha256='878f9ad080a40cdcec85b92242c4b5819eeb8f120ebc5c9f640935e24fc129d8')
    version('1.2.0', sha256='4ae0f37ece5f3b5baf9fa5b79b23482cb43a0207e380b5476cd4bd18e3ddd06d')
    version('1.1.0', sha256='49036087c1170c3fad026e45189f17092b8c584a9accb2d73d1854f494e223ae')
    version('1.0.3', sha256='10750207c1a9ad6f6e082d91dbff3920443bdaf1c344a782730489a9efa802f1')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-google-api-core@1.14:1.999', type=('build', 'run'))
