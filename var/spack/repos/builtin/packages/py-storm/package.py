# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStorm(PythonPackage):
    """Storm is an object-relational mapper (ORM) for Python"""
    homepage = "https://storm.canonical.com/"
    url      = "https://launchpad.net/storm/trunk/0.20/+download/storm-0.20.tar.gz"

    version('0.20', '8628503141f0f06c0749d607ac09b9c7')

    depends_on('py-setuptools', type='build')
