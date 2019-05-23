# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNatsort(PythonPackage):
    """Simple yet flexible natural sorting in Python."""

    homepage = "https://pypi.org/project/natsort/"
    url = "https://github.com/SethMMorton/natsort/archive/5.2.0.zip"

    version('5.2.0', '2ed2826550eef1f9ea3dd04f08b5da8b')
    version('5.1.1', '0525d4897fc98f40df5cc5a4a05f3c82')
    version('5.1.0', '518688548936d548775fb00afba999fb')
    version('5.0.3', '11147d75693995a946656927df7617d0')
    version('5.0.2', '1eb11a69086a5fb21d03f8189f1afed3')
    version('5.0.1', 'ca21c728bb3dd5dcfb010fa50b9c5e3c')
    version('5.0.0', 'fc7800fea50dcccbf8b116e1dff2ebf8')
    version('4.0.4', '7478ba31ec7fe554fcbfda41bb01f5ef')
    version('4.0.3', '2dc4fb1eb6ebfe4c9d95a12c2406df33')
    version('4.0.1', '659cf6ce95951003de0c85fc80b9f135')

    depends_on('py-setuptools', type=('build'))
