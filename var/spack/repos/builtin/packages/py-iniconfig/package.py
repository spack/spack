# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIniconfig(PythonPackage):
    """
    iniconfig: brain-dead simple parsing of ini files

    iniconfig is a small and simple INI-file parser module having a unique
    set of features:

    * tested against Python2.4 across to Python3.2, Jython, PyPy
    * maintains order of sections and entries
    * supports multi-line values with or without line-continuations
    * supports '#' comments everywhere
    * raises errors with proper line-numbers
    * no bells and whistles like automatic substitutions
    * iniconfig raises an Error if two sections have the same name.
    """

    homepage = "https://github.com/RonnyPfannschmidt/iniconfig"
    url      = "https://pypi.io/packages/source/i/iniconfig/iniconfig-1.1.1.tar.gz"

    version('1.1.1', sha256='bc3af051d7d14b2ee5ef9969666def0cd1a000e121eaea580d4a313df4b37f32')

    depends_on('py-setuptools', type='build')
