# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPint(PythonPackage):
    """Pint is a Python package to define, operate and manipulate physical
    quantities: the product of a numerical value and a unit of measurement.
    It allows arithmetic operations between them and conversions from and
    to different units."""

    homepage = "https://github.com/hgrecco/pint"
    url      = "https://github.com/hgrecco/pint/archive/0.11.tar.gz"

    version('0.11', sha256='78921f0a3446b610ee787252f8f76b96106728e675d9d3803eede2beb1d29cdb')
    version('0.10.1', sha256='a5bf18700a088b3da450c0ea103bd957f68cc7e67f30993b3f707b4b05a9cc05')
    version('0.10', sha256='d361575f05c481d93003b492f6eb280eb65a43aa033bca36a9ef7df53142711f')
    version('0.9', sha256='92220db7b46ff5f3cb0a8bd0967f43bb32c8b5ee3dc11d84e90ab1bd6c78f2f4')
    version('0.8.1', sha256='1146704c6f73577688789329a4ff75eb3a4a2b48a64bfa2e3c6ebbff8ee3416f')


    depends_on('py-setuptools', type='build')
