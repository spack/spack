# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyNestAsyncio(PythonPackage):
    """Patch asyncio to allow nested event loops."""

    homepage = "https://github.com/erdewit/nest_asyncio"
    pypi = "nest-asyncio/nest_asyncio-1.4.0.tar.gz"

    version('1.5.1', sha256='afc5a1c515210a23c461932765691ad39e8eba6551c055ac8d5546e69250d0aa')
    version('1.4.0', sha256='5773054bbc14579b000236f85bc01ecced7ffd045ec8ca4a9809371ec65a59c8')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
