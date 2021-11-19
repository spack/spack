# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCycler(PythonPackage):
    """Composable style cycles."""

    homepage = "https://matplotlib.org/cycler/"
    pypi = "cycler/cycler-0.11.0.tar.gz"

    version('0.11.0', sha256='9c87405839a19696e837b3b818fed3f5f69f16f1eec1a1ad77e043dcea9c772f')
    version('0.10.0', sha256='b6d217635e03024196225367b1a438996dbbf0271bec488f00584f0e7dc15cfa')

    depends_on('python@3.6:', when='@0.11:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', when='@:0.10', type=('build', 'run'))
