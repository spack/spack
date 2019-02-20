# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCmakeFormat(PythonPackage):
    """Source code formatter for cmake listfiles."""

    homepage = "https://github.com/cheshirekow/cmake_format"
    url      = "https://files.pythonhosted.org/packages/d8/3f/14e1a63402eeb664b35392b33450f27f0a7f8d00d8b0c26e8e108d9cef24/cmake_format-0.4.5.tar.gz"

    version('0.4.5', sha256='16602408c774cd989ecfa25883de4c2dbac937e3890b735be4aab76f9647875a')

    depends_on('py-setuptools', type='build')
