# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTern(PythonPackage):
    """
    Tern is a software package inspection tool that can create a Software Bill
    of Materials (SBoM) for containers.
    """

    pypi     = "tern/tern-2.8.0.tar.gz"
    git      = "https://github.com/tern-tools/tern.git"

    version('main', branch='main')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-pip', type='build')

    # this version has a setup.cfg warning that will prevent build success, use main
    version('2.8.0', sha256='dd7d8ad929ffe951b1f7f86310b9d5ba749b4306132c3611ff1d5a2c4d79d2bd')
