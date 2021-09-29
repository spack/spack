# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParsl(PythonPackage):
    """
    Simple data dependent workflows in Python
    """

    homepage = "https://github.com/Parsl/parsl"
    url      = "https://github.com/Parsl/parsl/archive/refs/tags/1.1.0.tar.gz"

    maintainers = ['hategan']

    version('1.1.0', sha256='6a623d3550329f028775950d23a2cafcb0f82b199f15940180410604aa5d102c')
    version('1.0.0', sha256='6e89cae32da7057ea3fbee278f6e11145697dc773f3a1b94acd2d63cbff7fc70')
    version('0.9.0', sha256='6bd29350fa13e3b5efbd7cd21b37b299eb31fe1501602494b4a2dbdaff0a8cbf')
    version('0.8.0', sha256='336f665a2cec879850d2e4328de9e91e1e881da13b62858003079a0d928829be')
    version('0.7.2', sha256='4fe2df4d2e49aaa6f03eab6a3798f25882cd08253df2246691a95a24ab9f7db0')
    version('0.7.1', sha256='7c208b6c194ada41cc9bbb0107b36cb1c101a39dcb170f50a87ab6ff688816ee')
    version('0.7.0', sha256='762e3ceb3b09f592eb0d0197b25833c4e50017cca595734e35de3398661f4e41')
    version('0.6.1', sha256='db63394bba57c0ca66c2e3498833af2a27c38640080e82e5c95b2a8f902b0154')
    version('0.6.0', sha256='e62536d22b68d25f94573c42884b5f7fee1e5981efe088dc7ff360790a951f95')
    version('0.5.2', sha256='0d00c109a80f70c656f0fe1c978323f0ea5e914f0253cfd3046c80663ec01545')
    version('0.5.1', sha256='ceef3225e4cd3a439f66b4fe0426455f3a291eae486f552e8e585ca0b7f85162')
    version('0.5.0', sha256='ed5c98fc06315aff5dd043c0c268f8e878f233d338cc1b9892080962515754bb')
    version('0.4.1', sha256='0f3c53308ea4407a73679fcd794a8f652c8f09e6d74e4f60ab1a215a1cf746ca')
    version('0.4.0', sha256='a9af70882d9881cfcf6265adcf29135159f4b7e7637620e95244f05ea187ed2f')
    version('0.3.1', sha256='b6b779fe408e2d5b4ebaf1caa15db3a351a4f4276812d11f5c17db6b4eba29c7')
    version('0.2.1', sha256='5689422462799a5377880bf759c6fd3abc5ef0a86343abec35a3a40d48f803f9')
    version('0.1.2', sha256='b849e1c85f06ab362383ef85b06a1f18cc73ac4cfaf3e79fbf6a27689957b321')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
