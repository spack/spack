# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLogilabCommon(PythonPackage):
    """Common modules used by Logilab projects"""
    homepage = "https://www.logilab.org/project/logilab-common"
    url      = "https://pypi.io/packages/source/l/logilab-common/logilab-common-1.2.0.tar.gz"

    version('1.2.0', sha256='d4e5cec3be3a89f06ff05e359a221e69bd1da33cb7096cad648ddcccea8465b7')

    extends('python', ignore=r'bin/pytest')
    depends_on("py-setuptools", type='build')
    depends_on("py-six", type=('build', 'run'))
