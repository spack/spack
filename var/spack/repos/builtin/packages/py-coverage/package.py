# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCoverage(PythonPackage):
    """ Testing coverage checker for python """

    homepage = "http://nedbatchelder.com/code/coverage/"
    url      = "https://pypi.io/packages/source/c/coverage/coverage-4.3.4.tar.gz"

    version('4.3.4', '89759813309185efcf4af8b9f7762630')
    version('4.0a6', '1bb4058062646148965bef0796b61efc')

    depends_on('py-setuptools', type='build')
