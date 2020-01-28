# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/rtfd/sphinx_rtd_theme/"
    url      = "https://pypi.io/packages/source/s/sphinx_rtd_theme/sphinx_rtd_theme-0.1.10a0.tar.gz"

    import_modules = ['sphinx_rtd_theme']

    version('0.4.3',  sha256='728607e34d60456d736cc7991fd236afb828b21b82f956c5ea75f94c8414040a')
    version('0.2.5b1',  sha256='d99513e7f2f8b9da8fdc189ad83df926b83d7fb15ad7ed07f24665d1f29d38da')
    version('0.1.10a0', sha256='1225df3fc8337b14d53779435381b7f7705b9f4819610f6b74e555684cee2ac4')

    depends_on('py-setuptools', type='build')
