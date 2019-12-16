# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZxcvbn(PythonPackage):
    """A realistic password strength estimator.

       This is a Python implementation of the library created by the team at
       Dropbox."""

    homepage = "https://github.com/dwolfhub/zxcvbn-python"
    url      = "https://github.com/dwolfhub/zxcvbn-python/archive/v4.4.25.tar.gz"

    version('4.4.25', 'e9bdae7193e6e13438cc9bb11eedd846')

    depends_on('py-setuptools', type='build')
