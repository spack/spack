# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColorspacious(PythonPackage):
    """`colorlog.ColoredFormatter` is a formatter for use with Python's 
    `logging` module that outputs records using terminal colors.
     """

    homepage = "https://github.com/borntyping/python-colorlog"
    url      = "https://pypi.io/packages/source/c/colorspacious/colorspacious-1.1.2.tar.gz"

    version('1.1.2', sha256='5e9072e8cdca889dac445c35c9362a22ccf758e97b00b79ff0d5a7ba3e11b618')

    depends_on('py-numpy')
