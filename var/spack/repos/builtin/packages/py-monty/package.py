# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMonty(PythonPackage):
    """Monty is the missing complement to Python."""

    homepage = "https://github.com/materialsvirtuallab/monty"
    url      = "https://pypi.io/packages/source/m/monty/monty-0.9.6.tar.gz"

    version('0.9.6', '406ea69fdd112feacfdf208624d56903')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
