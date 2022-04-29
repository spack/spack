# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyLizard(PythonPackage):
    """A code analyzer without caring the C/C++ header files.
       It works with Java, C/C++, JavaScript, Python, Ruby,
       Swift, Objective C. Metrics includes cyclomatic
       complexity number etc."""

    homepage = "http://www.lizard.ws/"
    pypi     = "lizard/lizard-1.17.9.tar.gz"

    version('1.17.9', sha256='76ee0e631d985bea1dd6521a03c6c2fa9dce5a2248b3d26c49890e9e085b7aed')

    depends_on('py-setuptools', type='build')
