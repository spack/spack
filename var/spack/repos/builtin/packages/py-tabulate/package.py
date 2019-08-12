# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTabulate(PythonPackage):
    """Pretty-print tabular data"""

    homepage = "https://bitbucket.org/astanin/python-tabulate"
    url      = "https://pypi.io/packages/source/t/tabulate/tabulate-0.7.7.tar.gz"

    version('0.7.7', '39a21aaa9c10be0749c545be34552559')

    depends_on('py-setuptools', type='build')
