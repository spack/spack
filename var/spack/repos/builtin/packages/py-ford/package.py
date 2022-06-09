# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack.package import *


class PyFord(PythonPackage):
    """FORD, standing for FORtran Documenter, is an automatic documentation generator for modern Fortran programs."""

    pypi     = "FORD/FORD-6.1.11.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('6.1.11', sha256='feb9a88040e717e84c632e4b023904ab36a463fc9a8ff80c8c7f86454e5d8043')

    depends_on('py-wheel@0.29:', type='build')

    depends_on('py-setuptools@48:', type='build')
    depends_on('py-setuptools-scm@4:5', type='build')
    depends_on('py-setuptools-scm-git-archive', type='build')

    # FIXME: Add additional dependencies if required.

    def global_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py
        # FIXME: If not needed, delete this function
        options = []
        return options

    def install_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py install
        # FIXME: If not needed, delete this function
        options = []
        return options
