# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPrettytable(PythonPackage):
    """PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually
    appealing ASCII tables.
    """

    homepage = "https://code.google.com/archive/p/prettytable/"
    url      = "https://pypi.io/packages/source/p/prettytable/prettytable-0.7.2.tar.gz"

    version('0.7.2', 'a6b80afeef286ce66733d54a0296b13b')

    depends_on("py-setuptools", type='build')
