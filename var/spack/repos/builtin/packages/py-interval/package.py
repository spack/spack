# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyInterval(PythonPackage):
    """Python interval and interval set implementation."""

    homepage = "https://pypi.org/project/interval/1.0.0/"
    url      = "https://pypi.io/packages/source/i/interval/interval-1.0.0.tar.bz2"

    version('1.0.0', '9dd55d218911e2b3c9cc9755608aeaf6')

    depends_on('python@:2', type=('build', 'run'))
