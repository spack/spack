# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXvfbwrapper(PythonPackage):
    """run headless display inside X virtual framebuffer (Xvfb)"""

    homepage = "https://pypi.python.org/pypi/xvfbwrapper/0.2.9"
    url      = "https://pypi.io/packages/source/x/xvfbwrapper/xvfbwrapper-0.2.9.tar.gz"

    version('0.2.9', '3f3cbed698606f4b14e76ccc7b5dd366')

    depends_on('py-setuptools', type='build')
    # Eventually add xvfb!
