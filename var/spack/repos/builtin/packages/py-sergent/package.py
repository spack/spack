# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter


class PySergent(PythonPackage):
    """
    Python Ssh to AWS EC2 helper
    """

    homepage = "https://github.com/chocobn69/sergent"
    pypi = 'Sergent/Sergent-1.2.12.tar.gz'
    maintainers = ['liuyangzhuan']
    
    version('1.2.12', sha256='2a16c4efc4613a0395f6815fb58567e061b4cab0bf54696aa7f0fb725171ad42')
    version('1.2.10', sha256='c8c788603dfd520b73d8153166a8cc55d3bdb3b97fa2374d14745a620eb206e1')    
    version('1.2.9', sha256='ed932cd0ed1a81b2d0642e8c51c5c077f01d06b3ed0653567158a9d3922339d0')
    version('1.2.8', sha256='9044704f90f8c389e66ec1e34ce6ef6074d67c784a724fe3981812028a66c207')
    version('1.2.7', sha256='e4ad274f10c9db90f858c5fbdcab0b0327ad1035441045fdf1080c1b5a4dfe22')
    version('1.2.6', sha256='1fb1a2a76199002651476be880480803b4fd6ac508306e630aa26362b906e0bd')
    version('1.2.5', sha256='6ebed242d5b04b673fd065ff268f888774587cf12803c11d6c4d0301b734f519')
    version('1.2.4', sha256='d17f62e86f6adc3c19d9da6389aff8340175579c2aad005275da8abd40d1d725')
    version('1.2.3', sha256='183b9a24f2ede1bfdae8715b6fbbc367b7eb4bc2ab64950d648220f36a65eb92')

    depends_on('py-setuptools', type='build')