# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydispatcher(PythonPackage):
    """Multi-producer-multi-consumer signal dispatching mechanism."""

    homepage = "http://pydispatcher.sourceforge.net/"
    url      = "https://pypi.io/packages/source/P/PyDispatcher/PyDispatcher-2.0.5.tar.gz"

    version('2.0.5', '1b9c2ca33580c2770577add7130b0b28')

    depends_on('py-setuptools', type='build')
