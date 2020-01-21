# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStorm(PythonPackage):
    """Storm is an object-relational mapper (ORM) for Python"""
    homepage = "https://storm.canonical.com/"
    url      = "https://launchpad.net/storm/trunk/0.20/+download/storm-0.20.tar.gz"

    version('0.20', sha256='0fa70043bb1a1c178c2f760db35f5956244cecf50dab7fb22d78be7507726603')

    depends_on('py-setuptools', type='build')
