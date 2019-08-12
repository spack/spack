# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMultiprocess(PythonPackage):
    """Better multiprocessing and multithreading in Python"""

    homepage = "https://github.com/uqfoundation/multiprocess"
    url = "https://pypi.io/packages/source/m/multiprocess/multiprocess-0.70.5.zip"

    version('0.70.5', 'bfe394368b1d98192f1f62cc0060be20')
    version('0.70.4', '443336d84c574106da6c67d4574b7614')

    depends_on('python@2.6:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
    depends_on('py-dill@0.2.6:', type=('build', 'run'))
