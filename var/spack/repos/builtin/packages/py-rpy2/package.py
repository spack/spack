# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRpy2(PythonPackage):
    """rpy2 is a redesign and rewrite of rpy. It is providing a low-level
       interface to R from Python, a proposed high-level interface,
       including wrappers to graphical libraries, as well as R-like
       structures and functions.

    """
    pypi = "rpy2/rpy2-2.5.4.tar.gz"

    version('3.4.2', sha256='8f7d1348b77bc45425b846a0d625f24a51a1c4f32ef2cd1c07a24222aa64e2e0')
    version('3.4.1', sha256='644360b569656700dfe13f59878ec1cf8c116c128d4f2f0bf96144031f95d2e2')
    version('3.4.0', sha256='d543e4a577961a24a79cfa3e0c31cdc0169cdcb4b7d80d035f4bcc9df8102d80')
    version('3.3.6', sha256='ce063f3286e717b3914728ad23ec7db0a0f117ba3ade5ada8a250700779f6e77')
    version('3.3.5', sha256='d2b1fb0e22924b08ba11acf07b93cec1842296c005e142834008bba25b3643af')
    version('3.3.4', sha256='763601b1c5d0195a53341c5b053b419e48eab163cdb8908e313ce7c1f207a3d1')
    version('3.3.3', sha256='ca578dae6df117d55e3e547b29a8247f3710b1246c322c6a6cec3249b823cf0b')
    version('3.3.2', sha256='2e12c99e56a1faa68f3b82a71b90e3389203c1e76cd53fe38946a8a7a31f9750')
    version('3.3.1', sha256='3f25f45d327e2244f0d0654a2cf11d3e8a402ecf73cab5662e37610ab47bbee8')
    version('3.3.0', sha256='08c90377dce51126311a5fa6e1cd7d1f451f759ce1f5e1755d8f44e8c40c1f23')
    version('3.2.7', sha256='db9c71eec3c91f44373839c24a1888a3999f2f342300e8e696e5dcc047d3df6d')
    version('3.2.6', sha256='1829c23fd9f6ac9dc8cf0ea14c1bc20a2a6e4a35c6f2c4726857dcd1310329dd')
    version('3.2.5', sha256='33fbb7c244fe4151a47899ab8f2f138ca0042d25755a3956d584453a8719d35e')
    version('3.2.4', sha256='3daf1a4b28c4e354ef989093f03b066908bf6e5082a6f4af72cc3fd928a28dc6')
    version('3.2.3', sha256='3cd58cffaa580f3a0053dc7e8be61e810e8b046c43a8948586010572744d0391')
    version('3.2.2', sha256='b71757776f1c652570f07243e708b6e6626456d3ee7d1f336357d4d393bd722c')
    version('3.2.1', sha256='cfba1b5d5ad56f9f52a0df4df8015a342043f113576003967fd760e063023ca6')
    version('3.2.0', sha256='18025f53c1a32b7b38ed319c81f8445b9a8809e0ecba210634b67764d68da978')
    version('3.1.0', sha256='ed4284df32d00b1fba5b1409e5df64b04b02d47aff543d6ef1dc211ab94e247f')
    version('3.0.5', sha256='c1fcd966780ebc3ea2400f73b558a801fbc17c09312f55d27b391b48fc24c8f9')
    version('3.0.4', sha256='2af5158a5d56af7f7bf5e54d8d7e87b6f115ff40f056d82f93cad0cbf6acc0cb')
    version('3.0.0', sha256='34efc2935d9015527837d6b1de29641863d184b19d39ad415d5384be8a015bce')
    version('2.9.4', sha256='be57f741d0c284b5d8785ab03dff0e829303e5ac30e548d5ceb46e05b168812e')
    version('2.8.6', sha256='004d13734a7b9a85cbc1e7a93ec87df741e28db1273ab5b0d9efaac04a9c5f98')
    version('2.5.6', sha256='d0d584c435b5ed376925a95a4525dbe87de7fa9260117e9f208029e0c919ad06')
    version('2.5.4', sha256='d521ecdd05cd0c31ab017cb63e9f63c29b524e46ec9063a920f640b5875f8a90')

    # FIXME: Missing dependencies:
    # ld: cannot find -licuuc
    # ld: cannot find -licui18

    # All versions
    depends_on('py-setuptools', type='build')
    depends_on('r',             type=('build', 'run'))

    # @3.0.0:
    depends_on('py-cffi@1.0.0:',   when='@3.0.0:', type=('build', 'run'))
    depends_on('py-simplegeneric', when='@3.0.0:', type=('build', 'run'))
    depends_on('py-pytest',        when='@3:', type=('build', 'run'))

    # @2.9.0:
    depends_on('r@3.3:',      when='@2.9.0:', type=('build', 'run'))
    depends_on('python@3.5:', when='@2.9.0:', type=('build', 'run'))
    depends_on('py-jinja2',   when='@2.9.0:', type=('build', 'run'))
    depends_on('py-six',      when='@2.9.0:2.9.999', type=('build', 'run'))

    # @:2.8.6
    depends_on('r@2.8:',           when='@:2.8.6', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:2',   type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
