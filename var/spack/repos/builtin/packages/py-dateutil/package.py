# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDateutil(PythonPackage):
    """Extensions to the standard Python datetime module."""
    homepage = "https://pypi.python.org/pypi/dateutil"
    url      = "https://pypi.io/packages/source/p/python-dateutil/python-dateutil-2.4.0.tar.gz"

    version('2.2',   'c1f654d0ff7e33999380a8ba9783fd5c')
    version('2.4.0', '75714163bb96bedd07685cdb2071b8bc')
    version('2.4.2', '4ef68e1c485b09e9f034e10473e5add2')
    version('2.5.2', 'eafe168e8f404bf384514f5116eedbb6')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
