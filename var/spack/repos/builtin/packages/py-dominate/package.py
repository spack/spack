# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDominate(PythonPackage):
    """Dominate is a Python library for creating and
    manipulating HTML documents using an elegant DOM API. It
    allows you to write HTML pages in pure Python very
    concisely, which eliminates the need to learn another
    template language, and lets you take advantage of the more
    powerful features of Python."""

    homepage = "https://github.com/Knio/dominate"
    url      = "https://files.pythonhosted.org/packages/29/23/edf8e470f1053245c1aa99d92c8a3da9e83f6c7d3eb39205486965425be5/dominate-2.6.0.tar.gz"
    # license = "spdx:LGPL-3.0"

    version('2.6.0', sha256='76ec2cde23700a6fc4fee098168b9dee43b99c2f1dd0ca6a711f683e8eb7e1e4')

    depends_on('python@2.7:2.9999,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
