# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyTblib(PythonPackage):
    """Traceback fiddling library. Allows you to pickle tracebacks."""

    homepage = "https://github.com/ionelmc/python-tblib"
    url      = "https://files.pythonhosted.org/packages/source/t/tblib/tblib-1.4.0.tar.gz"

    version('1.4.0', sha256='bd1ad564564a158ff62c290687f3db446038f9ac11a0bf6892712e3601af3bcd')

    depends_on('py-setuptools', type='build')
