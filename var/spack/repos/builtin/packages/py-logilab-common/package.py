# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLogilabCommon(PythonPackage):
    """Common modules used by Logilab projects"""
    homepage = "https://www.logilab.org/project/logilab-common"
    url      = "https://pypi.io/packages/source/l/logilab-common/logilab-common-1.2.0.tar.gz"

    version('1.2.0', 'f7b51351b7bfe052746fa04c03253c0b')

    extends('python', ignore=r'bin/pytest')
    depends_on("py-setuptools", type='build')
    depends_on("py-six", type=('build', 'run'))
