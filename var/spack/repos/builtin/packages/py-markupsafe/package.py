# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMarkupsafe(PythonPackage):
    """MarkupSafe is a library for Python that implements a unicode
    string that is aware of HTML escaping rules and can be used to
    implement automatic string escaping. It is used by Jinja 2, the
    Mako templating engine, the Pylons web framework and many more."""

    homepage = "http://www.pocoo.org/projects/markupsafe/"
    url      = "https://pypi.io/packages/source/M/MarkupSafe/MarkupSafe-1.0.tar.gz"

    import_modules = ['markupsafe']

    version('1.0',  '2fcedc9284d50e577b5192e8e3578355')
    version('0.23', 'f5ab3deee4c37cd6a922fb81e730da6e')
    version('0.22', 'cb3ec29fd5361add24cfd0c6e2953b3e')
    version('0.21', 'fde838d9337fa51744283f46a1db2e74')
    version('0.20', '7da066d9cb191a70aa85d0a3d43565d1')
    version('0.19', 'ccb3f746c807c5500850987006854a6d')

    depends_on('py-setuptools', type='build')
