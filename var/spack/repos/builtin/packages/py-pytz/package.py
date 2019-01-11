# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytz(PythonPackage):
    """World timezone definitions, modern and historical."""

    homepage = "http://pythonhosted.org/pytz"
    url      = "https://pypi.io/packages/source/p/pytz/pytz-2016.10.tar.gz"

    import_modules = ['pytz']

    version('2017.2',   'f89bde8a811c8a1a5bac17eaaa94383c',
            url="https://pypi.io/packages/source/p/pytz/pytz-2017.2.zip")
    version('2016.10',  'cc9f16ba436efabdcef3c4d32ae4919c')
    version('2016.6.1', 'b6c28a3b968bc1d8badfb61b93874e03')
    version('2014.10',  'eb1cb941a20c5b751352c52486aa1dd7')
    version('2014.9',   'd42bda2f4c1e873e02fbd1e4acfd1b8c')
    version('2015.4',   '417a47b1c432d90333e42084a605d3d8')
    version('2016.3',   'abae92c3301b27bd8a9f56b14f52cb29')

    depends_on('py-setuptools', type='build')
