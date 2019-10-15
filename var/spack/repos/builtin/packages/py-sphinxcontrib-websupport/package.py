# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('1.1.0', sha256='9de47f375baf1ea07cdb3436ff39d7a9c76042c10a769c52353ec46e4e8fc3b9')
    version('1.0.1', sha256='7a85961326aa3a400cd4ad3c816d70ed6f7c740acd7ce5d78cd0a67825072eb9')

    depends_on('py-setuptools', type='build')

    depends_on('py-pytest', type='test')
    depends_on('py-mock',   type='test')
