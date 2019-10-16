# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlask(PythonPackage):
    """A microframework based on Werkzeug, Jinja2 and good intentions"""

    homepage = "http://github.com/pallets/flask"
    url      = "https://pypi.io/packages/source/F/Flask/Flask-0.11.1.tar.gz"

    version('0.12.2', sha256='49f44461237b69ecd901cc7ce66feea0319b9158743dd27a2899962ab214dac1')
    version('0.12.1', sha256='9dce4b6bfbb5b062181d3f7da8f727ff70c1156cbb4024351eafd426deb5fb88')
    version('0.11.1', sha256='b4713f2bfb9ebc2966b8a49903ae0d3984781d5c878591cf2f7b484d28756b0e')

    depends_on('py-setuptools',         type='build')
    depends_on('py-werkzeug@0.7:',      type=('build', 'run'))
    depends_on('py-jinja2@2.4:',        type=('build', 'run'))
    depends_on('py-itsdangerous@0.21:', type=('build', 'run'))
    depends_on('py-click@2.0:',         type=('build', 'run'))
