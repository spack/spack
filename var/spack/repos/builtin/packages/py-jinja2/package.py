# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJinja2(PythonPackage):
    """Jinja2 is a template engine written in pure Python. It provides
    a Django inspired non-XML syntax but supports inline expressions
    and an optional sandboxed environment."""

    homepage = "http://jinja.pocoo.org/"
    url      = "https://pypi.io/packages/source/J/Jinja2/Jinja2-2.9.6.tar.gz"

    import_modules = ['jinja2']

    version('2.9.6', '6411537324b4dba0956aaa8109f3c77b')
    version('2.8',   'edb51693fe22c53cee5403775c71a99e')
    version('2.7.3', 'b9dffd2f3b43d673802fe857c8445b1a')
    version('2.7.2', 'df1581455564e97010e38bc792012aa5')
    version('2.7.1', '282aed153e69f970d6e76f78ed9d027a')
    version('2.7',   'c2fb12cbbb523c57d3d15bfe4dc0e8fe')

    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe', type=('build', 'run'))
    depends_on('py-babel@0.8:', type=('build', 'run'))  # optional, required for i18n
