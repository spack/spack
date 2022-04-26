# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPathlib(PythonPackage):
    """Object-oriented filesystem paths.

    Attention: this backport module isn't maintained anymore. If you want to
    report issues or contribute patches, please consider the pathlib2 project
    instead."""

    homepage = "https://pathlib.readthedocs.org/"
    pypi = "pathlib/pathlib-1.0.1.tar.gz"

    version('1.0.1', sha256='6940718dfc3eff4258203ad5021090933e5c04707d5ca8cc9e73c94a7894ea9f')

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')

    # This is a backport of the pathlib module from Python 3.4. Since pathlib is now
    # part of the standard library, this module isn't needed in Python 3.4+. Although it
    # can be installed, differences between this implementation and the standard library
    # implementation can cause other packages to fail. If it is installed, it ends up
    # masking the standard library and doesn't have the same features that the standard
    # library has in newer versions of Python.
    conflicts('^python@3.4:')
