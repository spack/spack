# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySqlalchemy(PythonPackage):
    """The Python SQL Toolkit and Object Relational Mapper"""

    homepage = 'http://www.sqlalchemy.org/'
    url      = "https://pypi.io/packages/source/S/SQLAlchemy/SQLAlchemy-1.3.9.tar.gz"

    version('1.3.9', sha256='272a835758908412e75e87f75dd0179a51422715c125ce42109632910526b1fd')
    version('1.2.19', sha256='5bb2c4fc2bcc3447ad45716c66581eab982c007dcf925482498d8733f86f17c7')
    version('1.1.18', sha256='8b0ec71af9291191ba83a91c03d157b19ab3e7119e27da97932a4773a3f664a9')
    version('1.0.12', '6d19ef29883bbebdcac6613cf391cac4')
