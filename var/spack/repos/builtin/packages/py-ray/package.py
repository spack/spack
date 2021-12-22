# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyRay(PythonPackage):
    """A system for parallel and distributed Python that unifies the ML
    ecosystem."""

    homepage = "https://github.com/ray-project/ray"
    url      = "https://github.com/ray-project/ray/archive/ray-0.8.7.tar.gz"

    version('1.9.1', sha256='394e34e6a1614ece96a3b2e9dd5bcf77fcfc246aaf3cce8c361f2b3ffff1242c')
    version('1.9.0', sha256='b6f519ec67044c71e6e961f909101b3ad3eaedf54adbe9f432584aa6f6ece1fe')
    version('1.8.0', sha256='b34d20f65aa9be5a0a82d468f67643ad9174a23ac5b90f1ab92c1e55fe5817d9')
    version('1.7.0', sha256='b7d565e4fe2ca1c145ee82aed47d5360ea0217c87d0a7b555e33a1d4b719ce42')
    version('1.6.0', sha256='b96a8d864b91dc1c2cfdc3d27602a3c9afaedbc7765330d6cba10c1f0ab56628')
    version('1.5.2', sha256='650d8bfa60400cb44b09be04730d5955f8b248e5db9a11a4216f1a66ff4b1255')
    version('1.5.1', sha256='f4aeeca4a8144e15179dfd4a2a5eea0256364f375c9e28572475f6b92cf614d0')
    version('1.5.0', sha256='88f6721c0fa77065ccbb8949f5f1dfa1d47ec683174d6e8e7b5ffc645a892a94')
    version('1.4.1', sha256='a5fcaeb405fc9e6ddf084d55d202f72c919e974dac736d0426a8b569f7022e4a')
    version('1.4.0', sha256='1ad04845dad6824220ad7750d666e7186f6b9186fb99294aae7d0e35f8e75018')
    version('1.3.0', sha256='66c65a6b7f5838726c908ebcc9d6c985f59ddbb0f22a700730422dde997d48d2')
    version('1.2.0', sha256='e4c9aa0cbfecf4d1112a43de473606a81f6fbba5c3f0b3013644268b366e2b75')
    version('1.1.0', sha256='c0fde1b6df563d8875e40aa12ad7559863753a3f7e11c976fea6d67d4adcb26c')
    version('1.0.1', sha256='e08ff04dc8bca99527dbc821446f8660cfe6cbc8c35db61410958b9aa9acee56')
    version('1.0.0', sha256='53aa83f6cc020a84d56192d4f4678e192a58ce33f12c5996343949d28780a788')
    version('0.8.7', sha256='2df328f1bcd3eeb4fa33119142ea0d669396f4ab2a3e78db90178757aa61534b')

    build_directory = 'python'

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('bazel@3.2.0', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.29.14:', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-aiohttp', type=('build', 'run'), when='@:1.0.1')
    depends_on('py-aiohttp@3.7', type=('build', 'run'), when='@1.1.0:1.7.0')
    depends_on('py-aiohttp@3.7:', type=('build', 'run'), when='@1.7.1:')
    depends_on('py-aioredis', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-colorama', type=('build', 'run'), when='@:1.5.2')
    depends_on('py-colorful', type=('build', 'run'), when='@:1.5.2')
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-google', type=('build', 'run'), when='@:1.0.1')
    depends_on('py-gpustat', type=('build', 'run'))
    depends_on('py-grpcio@1.28.1:', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-msgpack@1.0:1', type=('build', 'run'))
    depends_on('py-numpy@1.16:', type=('build', 'run'))
    depends_on('py-protobuf@3.8.0:', type=('build', 'run'))
    depends_on('py-py-spy@0.2.0:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-redis@3.3.2:3.4', type=('build', 'run'), when='@:1.0.1')
    depends_on('py-redis@3.5.0:4', type=('build', 'run'), when='@1.1.0:')
    depends_on('py-opencensus', type=('build', 'run'))
    depends_on('py-prometheus-client@0.7.1:', type=('build', 'run'))
    depends_on('py-cloudpickle', type=('build', 'run'), when='@1.3.0:')
    depends_on('py-pydantic@1.8.0:', type=('build', 'run'), when='@1.4.0:')
    depends_on('py-aiosignal', type=('build', 'run'), when='@1.9.0:')
    depends_on('py-smart-open', type=('build', 'run'), when='@1.9.0:')
    depends_on('py-frozenlist', type=('build', 'run'), when='@1.9.0:')
