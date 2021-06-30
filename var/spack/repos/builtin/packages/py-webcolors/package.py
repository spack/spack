# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWebcolors(PythonPackage):
    """Working with color names and values formats defined by HTML and CSS."""

    homepage = "https://pypi.org/project/webcolors/"
    url = "https://files.pythonhosted.org/packages/a7/df/b97bf02a97bbd5ed874fec7c5418bf0dd51e8d042ac46bbf2bf5983e89fd/webcolors-1.11.1.tar.gz"

    version('1.11.1', sha256='76f360636957d1c976db7466bc71dcb713bb95ac8911944dffc55c01cb516de6')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
