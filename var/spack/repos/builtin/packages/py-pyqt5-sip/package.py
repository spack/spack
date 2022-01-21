# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt5Sip(PythonPackage):
    """The sip module support for PyQt5."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi     = "PyQt5_sip/PyQt5_sip-12.9.0.tar.gz"

    version('12.9.0', sha256='d3e4489d7c2b0ece9d203ae66e573939f7f60d4d29e089c9f11daa17cfeaae32')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
