# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRecommonmark(PythonPackage):
    """A docutils-compatibility bridge to CommonMark.

    This allows you to write CommonMark inside of Docutils & Sphinx projects.

    Documentation is available on Read the Docs:
    http://recommonmark.readthedocs.org"""

    homepage = "https://github.com/readthedocs/recommonmark"
    url      = "https://files.pythonhosted.org/packages/f5/71/046160d730f664662d65b3f8b399b519ad378ffa4369ff3b6060cf1318d7/recommonmark-0.6.0.tar.gz"

    version('0.6.0', sha256='29cd4faeb6c5268c633634f2d69aef9431e0f4d347f90659fd0aab20e541efeb')

    depends_on('py-commonmark@0.8.1:')
    depends_on('py-docutils@011:')
    depends_on('py-sphinx@1.3.1:')
