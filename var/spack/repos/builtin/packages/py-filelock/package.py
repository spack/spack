# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFilelock(PythonPackage):
    """This package contains a single module, which implements a platform
    independent file lock in Python, which provides a simple way of
    inter-process communication"""

    homepage = "https://github.com/benediktschmitt/py-filelock"
    url = "https://github.com/benediktschmitt/py-filelock/archive/v3.0.4.tar.gz"

    version('3.0.4',  '3cafce82375c3b635f2c872acaf3a00b')
    version('3.0.3',  'e4bd69f15ebcc6d5a3d684cea3694840')
    version('3.0.1',  'cbf41ad3d89c89e2b752bc85b501dff6')
    version('3.0.0',  '29d199e8998ac324d0d7cab7aa814943')
    version('2.0.13', 'cdd0c4f3e905fbab76d1202ce8e8b454')
    version('2.0.12', 'fffda24b6cfd459ea5d2d5c335e949e2')
    version('2.0.11', '9e8cbbe18494d12647050bb32a7e624d')
    version('2.0.10', '1791e72bb19e503fdd0f365fb8ce2a4d')
    version('2.0.9',  'b0269e7f77a090cc0d5fc9cf5fbe6ac2')
    version('2.0.8',  '939ec6d4e2ecdc353a1f27fc452d8e8c')
