# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqi(PythonPackage):
    """pyqi (canonically pronounced pie chee) is a Python framework designed
       to support wrapping general commands in multiple types of interfaces,
       including at the command line, HTML, and API levels."""

    homepage = "https://pyqi.readthedocs.io"
    url      = "https://pypi.io/packages/source/p/pyqi/pyqi-0.3.2.tar.gz"

    version('0.3.2', '9507c06eeb22a816d963c860ad8e92ae')

    depends_on('py-setuptools', type='build')
