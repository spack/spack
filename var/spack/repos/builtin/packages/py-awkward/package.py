# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAwkward(PythonPackage):
    """Manipulate JSON-like data with NumPy-like idioms."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    pypi = "awkward/awkward-1.1.2.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers = ['vvolkl']

    version('master', branch='master')
    version('1.8.0', sha256='6655fa22d1b1d1dcb9ccee0d502350ab90c53467a10b540b7624422b594d2e72')
    version('1.7.0', sha256='e4e642dfe496d2acb245c90e37dc18028e25d5e936421e7371ea6ba0fde6435a')
    version('1.5.1', sha256='c0357c62223fefcfc7a7565389dbd4db900623bf10eccf2bc8e87586ec59b38d')
    version('1.5.0', sha256='3cb1b0e28f420232d894d89665d5c0c8241b99e56d806171f4faf5cdfec08ae1')
    version('1.4.0', sha256='25ae6114d5962c717cb87e3bc30a2f6eaa232b252cf8c51ba805b8f04664ae0d')
    version('1.3.0', sha256='b6021694adec9813842bad1987b837e439dabaf5b0dff9041201d238fca71fb4')
    version('1.2.3', sha256='7d727542927a926f488fa62d04e2c5728c72660f17f822e627f349285f295063')
    version('1.2.2', sha256='89f126a072d3a6eee091e1afeed87e0b2ed3c34ed31a1814062174de3cab8d9b')
    version('1.1.2', sha256='4ae8371d9e6d5bd3e90f3686b433cebc0541c88072655d2c75ec58e79b5d6943')
    version('1.0.2', sha256='3468cb80cab51252a1936e5e593c7df4588ea0e18dcb6fb31e3d2913ba883928')

    patch('pybind11.patch', when="@:1.2.2")
    patch('pybind11_02.patch', when="@1.2.3:")

    depends_on('py-setuptools@42.0:', type='build')
    depends_on('py-pyyaml', type='build')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-numpy@1.13.1:', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'link'))
    depends_on('dlpack', when="@1.0.0:")
    depends_on('rapidjson@:1.1.0')
    depends_on('cmake@3.13:', type='build')
    depends_on('py-wheel@0.36.0:', type='build', when='@:1.7.0')
