# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPureEval(PythonPackage):
    """This is a Python package that lets you safely evaluate certain AST nodes
    without triggering arbitrary code that may have unwanted side effects."""

    homepage = "https://github.com/alexmojaki/pure_eval"
    url      = "https://github.com/alexmojaki/pure_eval/archive/v0.1.0.tar.gz"

    version('0.1.0', sha256='67bed696eb316ba3801101eb173df9c49060061009000c1e959979c3d9fef16b')

    depends_on('python@3.5:3.9', type=('build', 'run'))
    depends_on('py-setuptools@44:',  type='build')
    depends_on('py-pip',         type=('build', 'run'))
    depends_on('py-wheel',       type=('build', 'run'))
