# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyke(PythonPackage):
    """Pyke introduces a form of Logic Programming (inspired by Prolog)
    to the Python community by providing a knowledge-based inference
    engine (expert system) written in 100% Python.
    """

    homepage = "http://sourceforge.net/projects/pyke"
    url      = "https://downloads.sourceforge.net/pyke/pyke3-1.1.1.zip"

    version('1.1.1', sha256='b877b390e70a2eacc01d97c3a992fde947276afc2798ca3ac6c6f74c796cb6dc')

    depends_on('python@3:')
