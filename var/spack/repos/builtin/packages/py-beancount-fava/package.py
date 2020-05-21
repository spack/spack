# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeancountFava(PythonPackage):
    """Fava is a web interface for the double-entry bookkeeping software
       Beancount with a focus on features and usability."""

    homepage = "https://beancount.github.io/fava/"
    pypi     = "fava/fava-1.18.tar.gz"

    version('1.18',  sha256='21336b695708497e6f00cab77135b174c51feb2713b657e0e208282960885bf5')

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
