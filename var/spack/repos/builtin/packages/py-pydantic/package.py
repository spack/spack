# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydantic(PythonPackage):
    """Data validation and settings management using Python type hinting."""

    homepage = "https://github.com/samuelcolvin/pydantic"
    pypi     = "pydantic/pydantic-1.8.2.tar.gz"

    version('1.8.2', sha256='26464e57ccaafe72b7ad156fdaa4e9b9ef051f69e175dbbb463283000c05ab7b')

    depends_on('python@3.6.1:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-dataclasses@0.6:', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4.3:', type=('build', 'run'))
