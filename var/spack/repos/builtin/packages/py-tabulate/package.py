# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTabulate(PythonPackage):
    """Pretty-print tabular data"""

    homepage = "https://bitbucket.org/astanin/python-tabulate"
    url      = "https://pypi.io/packages/source/t/tabulate/tabulate-0.7.7.tar.gz"

    version('0.7.7', sha256='83a0b8e17c09f012090a50e1e97ae897300a72b35e0c86c0b53d3bd2ae86d8c6')

    depends_on('py-setuptools', type='build')
