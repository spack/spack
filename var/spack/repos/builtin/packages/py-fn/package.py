# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFn(PythonPackage):
    """Functional programming in Python: implementation of missing features
    to enjoy FP."""

    homepage = "https://github.com/fnpy/fn.py"
    url      = "https://github.com/fnpy/fn.py/archive/v0.5.2.tar.gz"

    version('0.5.2', '48c168fe335e31fc6152ea0944741be2')

    depends_on('py-setuptools', type='build')
