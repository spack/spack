# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlaskBabel(PythonPackage):
    """Implements i18n and l10n support for Flask."""

    homepage = "https://pythonhosted.org/Flask-Babel/"
    url      = "https://pypi.io/packages/source/F/Flask-Babel/Flask-Babel-1.0.0.tar.gz"

    version('1.0.0',  sha256='d6a70468f9a8919d59fba2a291a003da3a05ff884275dddbd965f3b98b09ab3e')

    depends_on('python@2.7:2.8,3.6:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('py-flask',            type=('build', 'run'))
    depends_on('py-babel',            type=('build', 'run'))
    depends_on('py-pytz',             type=('build', 'run'))
    depends_on('py-werkzeug',         type=('build', 'run'))
