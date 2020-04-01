# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlake8Polyfill(PythonPackage):
    """flake8-polyfill is a package that provides some compatibility helpers
       for Flake8 plugins that intend to support Flake8 2.x and 3.x
       simultaneously.
    """
    homepage = "https://pypi.org/project/flake8-polyfill/"
    url      = "https://files.pythonhosted.org/packages/e6/67/1c26634a770db5c442e361311bee73cb3a177adb2eb3f7af8953cfd9f553/flake8-polyfill-1.0.2.tar.gz"

    version('1.0.2', sha256='e44b087597f6da52ec6393a709e7108b2905317d0c0b744cdca6208e670d8eda')

    extends('python', ignore='bin/(flake8|pyflakes|pycodestyle)')
    depends_on('py-flake8', type='run')
