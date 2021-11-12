# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIncremental(PythonPackage):
    """A small library that versions your Python projects."""

    homepage = "https://github.com/twisted/incremental"
    pypi     = "incremental/incremental-21.3.0.tar.gz"

    version('21.3.0', sha256='02f5de5aff48f6b9f665d99d48bfc7ec03b6e3943210de7cfc88856d755d6f57')

    depends_on('py-setuptools@44.1.1:', type='build')
    depends_on('py-typing@3.7.4.3:', type=('build', 'run'), when='@:3.4')
