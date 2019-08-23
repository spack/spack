# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOverpy(PythonPackage):
    """A Python Wrapper to access the Overpass API."""

    homepage = "https://github.com/DinoTools/python-overpy"
    url      = "https://pypi.io/packages/source/o/overpy/overpy-0.4.tar.gz"

    version('0.4', sha256='6e5bfcd9368f0c33a5d7615b18dbcac18444157f447639287c6743aa2de8964d')
    version('0.3.1', sha256='3c6f6afe262ccf50c983617fc4ec5f381c2e1f6391aa974fbcc39203802bc3ff')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-pytest', type='test')

    conflicts('python@3.0.0:3.1.99')
