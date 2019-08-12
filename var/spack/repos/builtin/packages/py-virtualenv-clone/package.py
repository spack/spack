# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVirtualenvClone(PythonPackage):
    """A script for cloning a non-relocatable virtualenv."""

    homepage = "https://github.com/edwardgeorge/virtualenv-clone"
    url      = "https://pypi.io/packages/source/v/virtualenv-clone/virtualenv-clone-0.2.6.tar.gz"

    version('0.2.6', 'fb03cd8c7a2be75937a13756d14068fc')

    depends_on('python@2.6:')
    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
