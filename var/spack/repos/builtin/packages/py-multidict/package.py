# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMultidict(PythonPackage):
    """Multidict is dict-like collection of key-value pairs where key
    might be occurred more than once in the container."""

    homepage = "https://github.com/aio-libs/multidict"
    url      = "https://github.com/aio-libs/multidict/archive/v4.7.6.tar.gz"

    version('5.1.0', sha256='1798708288851b808d2d03ea6046ca51bc44c228aaea12c9643a0a481ee41d8c')
    version('5.0.2', sha256='1847502cb325866a07ef3f3d06553f1dadeaf2de5691a39299720aace6681c71')
    version('5.0.1', sha256='f5c95d45882230f30df9e235971b2dc4c53532d0ab35978b149b69276ecd476c')
    version('5.0.0', sha256='1b324444299c3a49b601b1bf621fc21704e29066f6ac2b7d7e4034a4a18662a1')
    version('4.7.6', sha256='449035f89a12f189579ff83811424c71e4a39e335bcb8045145ad084b7bde2dc')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
