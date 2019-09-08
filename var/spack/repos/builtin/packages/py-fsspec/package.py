# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    url = "https://github.com/intake/filesystem_spec/archive/0.4.4.tar.gz"

    version('0.4.4', '27dfc3dab37d5c037683c7a3eaf7acd8b24ee56e4ce3edb14af54bdb43973d43')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
