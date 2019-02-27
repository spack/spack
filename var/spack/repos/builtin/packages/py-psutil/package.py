# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPsutil(PythonPackage):
    """psutil is a cross-platform library for retrieving information on
    running processes and system utilization (CPU, memory, disks, network)
    in Python."""

    homepage = "https://pypi.python.org/pypi/psutil"
    url      = "https://pypi.io/packages/source/p/psutil/psutil-5.4.5.tar.gz"

    version('5.5.1', '81d6969ba8392cd3b6f5cba6c4e77caa')
    version('5.4.5', '7d3d7954782bba4a400e106e66f10656')
    version('5.0.1', '153dc8be94badc4072016ceeac7808dc')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')
