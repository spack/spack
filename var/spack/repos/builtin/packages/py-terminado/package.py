# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTerminado(PythonPackage):
    """Terminals served to term.js using Tornado websockets"""

    pypi = "terminado/terminado-0.8.3.tar.gz"

    version('0.9.2', sha256='89e6d94b19e4bc9dce0ffd908dfaf55cc78a9bf735934e915a4a96f65ac9704c')
    version('0.9.1', sha256='3da72a155b807b01c9e8a5babd214e052a0a45a975751da3521a1c3381ce6d76')
    version('0.9.0', sha256='7ceea4c1644b0e95588d1d2ba09c5bf365b318c26d0a13ef6a5f2751a2f6efa3')
    version('0.8.3', sha256='4804a774f802306a7d9af7322193c5390f1da0abb429e082a10ef1d46e6fb2c2')
    version('0.8.2', sha256='de08e141f83c3a0798b050ecb097ab6259c3f0331b2f7b7750c9075ced2c20c2')
    version('0.8.1', sha256='55abf9ade563b8f9be1f34e4233c7b7bde726059947a593322e8a553cc4c067a')
    version('0.6',   sha256='2c0ba1f624067dccaaead7d2247cfe029806355cef124dc2ccb53c83229f0126')

    depends_on('py-tornado@4:', type=('build', 'run'))
    depends_on('py-ptyprocess', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.8.2:', type=('build', 'run'))
