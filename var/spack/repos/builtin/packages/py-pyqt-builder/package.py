# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPyqtBuilder(PythonPackage):
    """The PEP 517 compliant PyQt build system."""

    homepage = "https://www.riverbankcomputing.com/hg/PyQt-builder/"
    pypi = "PyQt-builder/PyQt-builder-1.12.2.tar.gz"

    version('1.12.2', sha256='f62bb688d70e0afd88c413a8d994bda824e6cebd12b612902d1945c5a67edcd7')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools@30.3:', type='build')
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-sip@6.3:6', type=('build', 'run'))
