##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyCookiecutter(PythonPackage):
    """A command-line utility that creates projects from
    cookiecutters (project templates).
    E.g. Python package projects, jQuery plugin projects."""

    homepage = "https://cookiecutter.readthedocs.io/en/latest/"
    url      = "https://github.com/audreyr/cookiecutter/archive/1.6.0.tar.gz"

    version('1.6.0', sha256='0c9018699b556b83d7c37b27fe0cc17485b90b6e1f47365b3cdddf77f6ca9d36')

    depends_on('py-setuptools', type='build')
    depends_on('py-future')
    depends_on('py-binaryornot')
    depends_on('py-jinja2')
    depends_on('py-click')
    depends_on('py-whichcraft')
    depends_on('py-poyo')
    depends_on('py-jinja2-time')
    depends_on('py-requests')
