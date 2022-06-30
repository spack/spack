# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKoji(PythonPackage):
    """Python library to access the Koji system for building and tracking RPMS."""

    pypi = "koji/koji-1.29.0.tar.gz"

    version('1.29.0', sha256='7db1ea4f68dd94d556c612e40bbfc2268164bfebc4a4cd08b63971bddaa686bc')

    extends('python', ignore=r'bin/pytest')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
