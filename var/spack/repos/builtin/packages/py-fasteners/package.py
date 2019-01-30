# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    url      = "https://pypi.io/packages/source/f/fasteners/fasteners-0.14.1.tar.gz"

    version('0.14.1', 'fcb13261c9b0039d9b1c4feb9bc75e04')

    depends_on('py-setuptools',     type='build')
    depends_on('py-monotonic@0.1:', type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))
