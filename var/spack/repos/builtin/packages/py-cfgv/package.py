# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv"
    url      = "https://files.pythonhosted.org/packages/84/7a/84fe8269f1bafb906b660917820d329c863b845b73b2e150de8900837470/cfgv-1.4.0.tar.gz"

    version('1.4.0', sha256='39d9055c47e3932908fe25abd5807e21dc002630db01c7a5f05738d027e2b706')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
