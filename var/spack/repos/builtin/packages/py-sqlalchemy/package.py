# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySqlalchemy(PythonPackage):
    """The Python SQL Toolkit and Object Relational Mapper"""

    homepage = 'http://www.sqlalchemy.org/'
    pypi = "SQLAlchemy/SQLAlchemy-1.3.9.tar.gz"

    # 'sqlalchemy.testing.suite' requires 'pytest'
    # Attempt to import everything other than 'sqlalchemy.testing'
    # to avoid unnecessary 'pytest' dependency
    import_modules = [
        'sqlalchemy', 'sqlalchemy.connectors', 'sqlalchemy.databases',
        'sqlalchemy.util', 'sqlalchemy.ext', 'sqlalchemy.ext.declarative',
        'sqlalchemy.dialects', 'sqlalchemy.dialects.sybase',
        'sqlalchemy.dialects.postgresql', 'sqlalchemy.dialects.oracle',
        'sqlalchemy.dialects.sqlite', 'sqlalchemy.dialects.mysql',
        'sqlalchemy.dialects.mssql', 'sqlalchemy.dialects.firebird', 'sqlalchemy.orm',
        'sqlalchemy.engine', 'sqlalchemy.pool', 'sqlalchemy.event', 'sqlalchemy.sql'
    ]

    version('1.4.20', sha256='38ee3a266afef2978e82824650457f70c5d74ec0cadec1b10fe5ed6f038eb5d0')
    version('1.3.19', sha256='3bba2e9fbedb0511769780fe1d63007081008c5c2d7d715e91858c94dbaa260e')
    version('1.3.9', sha256='272a835758908412e75e87f75dd0179a51422715c125ce42109632910526b1fd')
    version('1.2.19', sha256='5bb2c4fc2bcc3447ad45716c66581eab982c007dcf925482498d8733f86f17c7')
    version('1.2.10', sha256='72325e67fb85f6e9ad304c603d83626d1df684fdf0c7ab1f0352e71feeab69d8')
    version('1.1.18', sha256='8b0ec71af9291191ba83a91c03d157b19ab3e7119e27da97932a4773a3f664a9')
    version('1.0.12', sha256='6679e20eae780b67ba136a4a76f83bb264debaac2542beefe02069d0206518d1')

    depends_on('python@2.7:2.8,3.6:', when='@1.4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@:1.3', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-importlib-metadata', when='@1.4.0: ^python@:3.7', type='run')
    depends_on('py-greenlet@:0.4.16,0.4.18:', when='@1.4.0: ^python@3:', type='run')

    variant('backend', description='Python modules for database access',
            values=any_combination_of('mysql', 'pymysql', 'postgresql'))

    # >=1.4.0
    depends_on('py-mysqlclient@1.4:',       when='backend=mysql @1.4: ^python@3:',     type=('build', 'run'))
    depends_on('py-mysqlclient@1.4:,:1', when='backend=mysql @1.4: ^python@:2.7',   type=('build', 'run'))
    depends_on('py-pymysql',                when='backend=pymysql @1.4: ^python@3:',   type=('build', 'run'))
    depends_on('py-pymysql@:0',             when='backend=pymysql @1.4: ^python@:2.7', type=('build', 'run'))
    depends_on('py-psycopg2@2.7:',          when='backend=postgresql @1.4:',           type=('build', 'run'))

    # < 1.4.0
    depends_on('py-mysqlclient', when='backend=mysql @:1.3',      type=('build', 'run'))
    depends_on('py-pymysql',     when='backend=pymysql @:1.3',    type=('build', 'run'))
    depends_on('py-psycopg2',    when='backend=postgresql @:1.3', type=('build', 'run'))
