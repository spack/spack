# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    url      = "https://pypi.io/packages/source/v/virtualenv/virtualenv-15.1.0.tar.gz"

    version('16.4.1', sha256='5a3ecdfbde67a4a3b3111301c4d64a5b71cf862c8c42958d30cf3253df1f29dd')
    version('16.0.0', '4feb74ee26255dd7e62e36ce96bcc4c6')
    version('15.1.0', '44e19f4134906fe2d75124427dc9b716')
    version('15.0.1', '28d76a0d9cbd5dc42046dd14e76a6ecc')
    version('13.0.1', '1ffc011bde6667f0e37ecd976f4934db')
    version('1.11.6', 'f61cdd983d2c4e6aeabb70b1060d6f49')

    depends_on('python@2.6:')

    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
