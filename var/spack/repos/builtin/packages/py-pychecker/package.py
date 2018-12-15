# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPychecker(PythonPackage):
    """Python source code checking tool."""
    homepage = "http://pychecker.sourceforge.net/"
    url      = "http://sourceforge.net/projects/pychecker/files/pychecker/0.8.19/pychecker-0.8.19.tar.gz"

    version('0.8.19', 'c37182863dfb09209d6ba4f38fce9d2b')
