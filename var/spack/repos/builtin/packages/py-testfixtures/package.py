# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTestfixtures(PythonPackage):
    """Testfixtures is a collection of helpers and mock objects that are useful
    when writing automated tests in Python."""

    homepage = "https://github.com/Simplistix/testfixtures"
    url      = "https://github.com/Simplistix/testfixtures/archive/6.16.0.zip"

    version('6.17.1', sha256='8c65b000ae8c9bac881b19f57edfc27750165a7743f319238611dbe1b9b3ec00')
    version('6.17.0', sha256='2bf208c54b619a0664f7735636f99ddaa660f9a4bd9ee6e1869dc5f2db2f86b1')
    version('6.16.0', sha256='6b5bbca4f7d5692ca4566c60c0383b121d9f1cfecbc3de8442c499a63c264eb8')

    depends_on('py-setuptools', type='build')
