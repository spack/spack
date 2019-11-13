# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVoluptuous(PythonPackage):
    """Voluptous, despite the name, is a Python data validation library."""
    homepage = "https://github.com/alecthomas/voluptuous"
    url      = "https://github.com/alecthomas/voluptuous/archive/0.11.5.tar.gz"

    version('0.11.5', sha256='01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4')

    depends_on('py-setuptools', type='build')
