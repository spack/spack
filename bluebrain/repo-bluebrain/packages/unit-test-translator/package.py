# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UnitTestTranslator(PythonPackage):
    """Transforms the XML unit test output from CMake to proper JUnit XML.
    """

    homepage = "https://bbpgitlab.epfl.ch/hpc/unit-test-translator"
    git      = "git@bbpgitlab.epfl.ch:hpc/unit-test-translator.git"

    version('develop', branch='main')
    version('0.0.2', tag='v0.0.2')
    version('0.0.1', tag='v0.0.1')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
