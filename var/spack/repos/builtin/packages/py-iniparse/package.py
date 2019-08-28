# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIniparse(PythonPackage):
    """Accessing and Modifying INI files"""

    homepage = "https://github.com/candlepin/python-iniparse"
    url      = "https://pypi.io/packages/source/i/iniparse/iniparse-0.4.tar.gz"

    version('0.4', sha256='abc1ee12d2cfb2506109072d6c21e40b6c75a3fe90a9c924327d80bc0d99c054')
