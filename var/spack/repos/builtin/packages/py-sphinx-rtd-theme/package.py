# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/rtfd/sphinx_rtd_theme/"
    url      = "https://pypi.io/packages/source/s/sphinx_rtd_theme/sphinx_rtd_theme-0.1.10a0.tar.gz"

    import_modules = ['sphinx_rtd_theme']

    version('0.2.5b1',  '0923473a43bd2527f32151f195f2a521')
    version('0.1.10a0', '83bd95cae55aa8b773a8cc3a41094282')

    depends_on('py-setuptools', type='build')
