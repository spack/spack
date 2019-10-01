# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZipp(PythonPackage):
    """Backport of pathlib-compatible object wrapper for zip files."""

    homepage = "https://github.com/jaraco/zipp"
    url      = "https://pypi.io/packages/source/z/zipp/zipp-0.6.0.tar.gz"

    version('0.6.0', sha256='3718b1cbcd963c7d4c5511a8240812904164b7f381b647143a89d3b98f9bcd8e')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-more-itertools', type=('build', 'run'))
