# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPem(PythonPackage):
    """
    pem is an MIT-licensed Python module for parsing and splitting of PEM
    files, i.e. Base64 encoded DER keys and certificates.

    It runs on Python 2.7, 3.5+, and PyPy, has no dependencies, and does not
    attempt to interpret the certificate data in any way.

    It’s born from the need to load keys, certificates, trust chains, and DH
    parameters from various certificate deployments: some servers (like Apache)
    expect them to be a separate file, others (like nginx) expect them
    concatenated to the server certificate and finally some (like HAProxy)
    expect key, certificate, and chain to be in one file. With pem, your Python
    application can cope with all of those scenarios:

    import pem
    certs = pem.parse_file("chain.pem")
    certs
    [<Certificate(PEM string with SHA-1 digest '...')>, <Certificate(PEM string
    with SHA-1 digest '...')>]
    str(certs[0])
    '-----BEGIN CERTIFICATE-----\n...'

    Additionally to the vanilla parsing code, pem also contains helpers for
    Twisted that save a lot of boilerplate code.

    pem’s documentation lives at Read the Docs, the code on GitHub.
    """

    homepage = "https://pem.readthedocs.io/en/stable/"
    url      = "https://github.com/hynek/pem/archive/20.1.0.tar.gz"

    version('20.1.0', sha256='140df7388f72bdf95d5a40e152cfda4fd62856b8320a9a808ffdc2bee37d5c36')
    version('19.3.0', sha256='22c526314db05559d5a6b0661aa6a21f26a1ad9f6f10a6ba2d386534ad12b175')
    version('19.2.0', sha256='93772e1574c8ff3442e553025fe42ed66cea3abff7ce75363baffa8eb606e596')
    version('19.1.0', sha256='da4035ce675c0bd572e9e1b75e30c38553610a7d861460299ee18d72928379de')
    version('18.2.0', sha256='18d8440b62ae264343da72b0f6df934291c2fcdaffbeaf249150a3fe76751ed5')
    version('18.1.0', sha256='6bcb3474d112c9dc4aca6900e6b4967cbc1db11f693c8e535f728be2f5620604')
    version('17.1.0', sha256='f33191c11e0bcba2c3d36dc5cfeefe5cc692778a4d33e2a51e56ed7c2c22a4ce')
    version('16.1.0', sha256='5204e85da8561e98f96fa0be9aec6e15ee9fd40499fb4ec533e0513a42effa0b')
    version('16.0.0', sha256='a7a00aa4e1e82d39ae78f7705b0e5dfc7d7b2cf8a16ee073c24af330f75b421e')
    version('15.0.0', sha256='e93e3cfc017fca98223e9842f9ce5df1ad58bf5b4fb1fe82092fd1b778c187e1')

    depends_on('py-setuptools', type='build')
