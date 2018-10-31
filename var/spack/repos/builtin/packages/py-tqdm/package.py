# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    url      = "https://pypi.io/packages/source/t/tqdm/tqdm-4.8.4.tar.gz"

    version('4.8.4', 'b30a0aa20641d239296eab1c48a06b4e')

    depends_on('py-setuptools', type='build')
