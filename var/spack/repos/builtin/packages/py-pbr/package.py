# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
       behaviors into your setuptools run."""
    homepage = "https://pypi.python.org/pypi/pbr"
    url      = "https://pypi.io/packages/source/p/pbr/pbr-1.10.0.tar.gz"

    version('3.1.1', '4e82c2e07af544c56a5b71c801525b00')
    version('2.0.0', 'dfc1c3788eff06acfaade6f1655fa490')
    version('1.10.0', '8e4968c587268f030e38329feb9c8f17')
    version('1.8.1', 'c8f9285e1a4ca6f9654c529b158baa3a')

    depends_on('py-setuptools', type='build')
    # Only needed for py<3.4, however when='^python@:3.4.2' syntax might be
    # broken, if this fails, remove the when-clause
    depends_on('py-enum34', type='build', when='^python@:3.3')
