# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCookiecutter(PythonPackage):
    """A command-line utility that creates projects from cookiecutters
    (project templates).  E.g. Python package projects, jQuery plugin
    projects."""

    homepage = "https://cookiecutter.readthedocs.io/en/latest/"
    url      = "https://github.com/audreyr/cookiecutter/archive/1.6.0.tar.gz"

    version('1.7.2', sha256='32d176621bbbe76f11012e015930d2382f0fbe803362091e79a5dddbf5612abc')
    version('1.7.1', sha256='768aab727996758c9fa090876335f9912081d191b184816e5fc16f081ef110d6')
    version('1.7.0', sha256='975c578050a040e77c9a68a49ba420137d8da820d8ebf109342144f73a02722d')
    version('1.6.0', sha256='0c9018699b556b83d7c37b27fe0cc17485b90b6e1f47365b3cdddf77f6ca9d36')

    depends_on('py-setuptools', type='build')
    depends_on('py-future@0.15.2:', type=('build', 'run'))
    depends_on('py-binaryornot@0.2.0:', type=('build', 'run'))
    depends_on('py-jinja2@2.7:', type=('build', 'run'))
    depends_on('py-click@5.0:', type=('build', 'run'))
    depends_on('py-whichcraft@0.4.0:', type=('build', 'run'))
    depends_on('py-poyo@0.1.0:', type=('build', 'run'))
    depends_on('py-jinja2-time@0.1.0:', type=('build', 'run'))
    depends_on('py-requests@2.18.0:', type=('build', 'run'))
