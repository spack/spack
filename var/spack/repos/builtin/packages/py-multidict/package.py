# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMultidict(PythonPackage):
    """Multidict is dict-like collection of key-value pairs where key
    might be occurred more than once in the container."""

    homepage = "https://github.com/aio-libs/multidict"
    url      = "https://github.com/aio-libs/multidict/archive/v4.7.6.tar.gz"

    version('5.2.0', sha256='70039c8d0f4883816de230619c9d4ee1b8527b3628a42783e8bc26de4fee1154')
    version('5.1.0', sha256='1798708288851b808d2d03ea6046ca51bc44c228aaea12c9643a0a481ee41d8c')
    version('4.7.6', sha256='449035f89a12f189579ff83811424c71e4a39e335bcb8045145ad084b7bde2dc')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools@40:', type='build', when='@5.1.0:')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@5.1.0:')
