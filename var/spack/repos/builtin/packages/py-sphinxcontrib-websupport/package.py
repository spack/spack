# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribWebsupport(PythonPackage):
    """sphinxcontrib-webuspport provides a Python API to easily integrate
    Sphinx documentation into your Web application."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-websupport/sphinxcontrib-websupport-1.0.1.tar.gz"

    # FIXME: These import tests don't work for some reason
    # import_modules = [
    #     'sphinxcontrib', 'sphinxcontrib.websupport',
    #     'sphinxcontrib.websupport.storage', 'sphinxcontrib.websupport.search'
    # ]

    version('1.0.1', '84df26463b1ba65b07f926dbe2055665')

    depends_on('py-setuptools', type='build')

    depends_on('py-pytest', type='test')
    depends_on('py-mock',   type='test')
