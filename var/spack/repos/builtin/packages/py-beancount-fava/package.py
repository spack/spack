# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeancountFava(PythonPackage):
    """Fava is a web interface for the double-entry bookkeeping software
       Beancount with a focus on features and usability."""

    homepage = "https://beancount.github.io/fava/"
    url      = "https://pypi.io/packages/source/f/fava/fava-1.15.tar.gz"
    git      = "https://github.com/beancount/fava.git"

    version('master', branch='master')
    version('1.15',  sha256='ff691c328cc524fb752c20b5c4ad2f23817caa2e0d9ec791f00a47e96a84ee0c')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))

    depends_on('py-pkgconfig',           type=('build', 'run'))
    depends_on('py-werkzeug@0.15.0:',    type=('build', 'run'))
    depends_on('py-simplejson@3.2.0:',   type=('build', 'run'))
    depends_on('py-markdown2@2.3.0:',    type=('build', 'run'))
    depends_on('py-click',               type=('build', 'run'))
    depends_on('py-jinja2@2.10:',        type=('build', 'run'))
    depends_on('py-flask@0.10.1:',       type=('build', 'run'))
    depends_on('py-flask-babel@1.0.0:',  type=('build', 'run'))
    depends_on('py-cheroot',             type=('build', 'run'))
    depends_on('py-beancount@2.1.3:',    type=('build', 'run'))
