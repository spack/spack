# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyRanger(PythonPackage):
    """A VIM-inspired filemanager for the console"""

    homepage = "http://ranger.nongnu.org/"
    url      = "https://github.com/ranger/ranger/archive/v1.7.2.tar.gz"

    version('1.7.2', '27805c3ab7ec4b129e1b93249506d925')

    depends_on('python@2.6:')
