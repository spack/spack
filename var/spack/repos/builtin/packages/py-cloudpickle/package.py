# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCloudpickle(PythonPackage):
    """Extended pickling support for Python objects."""

    homepage = "https://github.com/cloudpipe/cloudpickle"
    url      = "https://pypi.io/packages/source/c/cloudpickle/cloudpickle-0.5.2.tar.gz"

    import_modules = ['cloudpickle']

    version('0.5.2', 'd0f6fc27882f865f2eb185fb0a32c84b')

    depends_on('py-setuptools', type='build')

    def test(self):
        # PyPI tarball does not come with unit tests
        pass
