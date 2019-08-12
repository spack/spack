# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxBootstrapTheme(PythonPackage):
    """Sphinx Bootstrap Theme."""

    homepage = "https://pypi.python.org/pypi/sphinx-bootstrap-theme/"
    url      = "https://pypi.io/packages/source/s/sphinx-bootstrap-theme/sphinx-bootstrap-theme-0.4.13.tar.gz"

    version('0.4.13', '32e513a9c8ffbb8c1e4b036e8f74fb51')

    depends_on('py-setuptools', type='build')
