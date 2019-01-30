# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVcversioner(PythonPackage):
    """Vcversioner: Take version numbers from version control."""

    homepage = "https://github.com/habnabit/vcversioner"
    url      = "https://pypi.io/packages/source/v/vcversioner/vcversioner-2.16.0.0.tar.gz"

    version('2.16.0.0', 'aab6ef5e0cf8614a1b1140ed5b7f107d')

    depends_on('py-setuptools', type='build')
