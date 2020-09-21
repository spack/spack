# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-lmodule
#
# You can edit this file again by typing:
#
#     spack edit py-lmodule
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyLmodule(PythonPackage):
    """Lmodule is a Python API for Lmod module system. It's primary purpose is to help
    automate module testing. Lmodule uses Lmod spider tool to query all modules inorder
    to automate module testing. Lmodule can be used with environment-modules to interact
    with module command with limited support for module interface."""

    homepage = "https://lmodule.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/l/lmodule/lmodule-0.1.0.tar.gz"
    git      = "https://github.com/buildtesters/lmodule"

    maintainers = ['shahzebsiddiqui']

    version('0.1.0', sha256='cac8f3dad2df27b10e051b2c56ccbde1fcdd7044af594d13fd2e4144d3d46a29')

    depends_on('python@3.6.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

