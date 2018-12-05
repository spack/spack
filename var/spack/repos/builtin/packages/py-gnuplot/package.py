# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGnuplot(PythonPackage):
    """Gnuplot.py is a Python package that allows you to create graphs from
       within Python using the gnuplot plotting program."""
    homepage = "http://gnuplot-py.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/gnuplot-py/Gnuplot-py/1.8/gnuplot-py-1.8.tar.gz"

    version('1.8', 'abd6f571e7aec68ae7db90a5217cd5b1')

    depends_on('py-numpy', type=('build', 'run'))
