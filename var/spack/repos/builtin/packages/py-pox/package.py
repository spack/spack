# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPox(PythonPackage):
    """Utilities for filesystem exploration and automated builds."""

    homepage = "https://github.com/uqfoundation/pox"
    url      = "https://pypi.io/packages/source/p/pox/pox-0.2.3.zip"

    version('0.2.3', 'fcdfd9a9ab0f72367258b675554f6a83')
    version('0.2.2', 'e1e2ce99a63d7226ea3c1a2ce389610d')
    version('0.2.1', '517dc13c2bc2429d36a0c636f3ce42db')

    depends_on('python@2.5:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
