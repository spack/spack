# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBoltons(PythonPackage):
    """When they're not builtins, they're boltons.

    Functionality that should be in the standard library. Like builtins,
    but Boltons.

    Otherwise known as, "everyone's util.py," but cleaned up and tested.
    """
    homepage = "https://boltons.readthedocs.io/"
    url = "https://pypi.io/packages/source/b/boltons/boltons-16.5.1.tar.gz"

    version('16.5.1', '014b10f240fa509fc333ebff4978111b')

    depends_on('py-setuptools', type='build')
