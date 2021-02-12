# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "http://ipython.org"
    pypi = "qtconsole/qtconsole-4.2.1.tar.gz"

    version('5.0.2', sha256='404994edfe33c201d6bd0c4bd501b00c16125071573c938533224992bea0b30f')
    version('5.0.1', sha256='4d7dd4eae8a90d0b2b19b31794b30f137238463998989734a3acb8a53b506bab')
    version('5.0.0', sha256='a232414549b2208041175ef992c4275d0b97e6839bf217a7c52490a755f6dd21')
    version('4.7.7', sha256='f236ead8711dba0702507dd8fad473c7216a86eefa6098eff8ec4b54f57d7804')
    version('4.7.6', sha256='6c24397c19a49a5cf69582c931db4b0f6b00a78530a2bfd122936f2ebfae2fef')
    version('4.7.5', sha256='f5cb275d30fc8085e2d1d18bc363e5ba0ce6e559bf37d7d6727b773134298754')
    version('4.7.4', sha256='fd48bf1051d6e69cec1f9e2596cfaa94e3c726c70c5d848681ebce10c029f5fd')
    version('4.7.3', sha256='8f5ae5571f0e921db9f2d12613ed667c350ee22c7db598d9bbbe143e8533f932')
    version('4.7.2', sha256='d7834598825169fc322390fdfd96bf791833ded21bf22803f083662edbbf3d75')
    version('4.7.1', sha256='d51c1c51c81fbd1fac62b2d4bdc8b54fb6b7cbe6cbf70c3baeea11516525c956')
    version('4.7.0', sha256='a7a9571ffe8adf07ede8660ee65bfacb10af64d6aa633a879e1ba0d70117f8a4')
    version('4.6.0', sha256='654f423662e7dfe6a9b26fac8ec76aedcf742c339909ac49f1f0c1a1b744bcd1')
    version('4.5.5', sha256='b91e7412587e6cfe1644696538f73baf5611e837be5406633218443b2827c6d9')
    version('4.5.4', sha256='756bdcb6de6900dc50b14430accff2e47b846c3e7820e04075d4067b4c0ab52f')
    version('4.5.3', sha256='84b43391ad0a54d91a628dbcd95562651052ea20457a75af85a66fea35397950')
    version('4.5.2', sha256='767eb9ec3f9943bc84270198b5ff95d2d86d68d6b57792fafa4df4fc6b16cd7c')
    version('4.5.1', sha256='4af84facdd6f00a6b9b2927255f717bb23ae4b7a20ba1d9ef0a5a5a8dbe01ae2')
    version('4.2.1', sha256='25ec7d345528b3e8f3c91be349dd3c699755f206dc4b6ec668e2e5dd60ea18ef')

    variant('doc', default=False, description='Build documentation')

    depends_on('python@2.7:2.8,3.3:',    type=('build', 'run'))
    depends_on('py-ipykernel@4.1:',      type=('build', 'run'))
    depends_on('py-jupyter-client@4.1:', type=('build', 'run'))
    depends_on('py-jupyter-core',        type=('build', 'run'))
    depends_on('py-pygments',            type=('build', 'run'))
    depends_on('py-traitlets',           type=('build', 'run'))
    depends_on('py-ipython-genutils',    type=('build', 'run'), when='@4.5.1:')
    depends_on('py-sphinx@1.3:',         type=('build', 'run'), when='+docs')
    depends_on('py-pyqt5',               type='run')
