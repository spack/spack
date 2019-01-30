# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyyaml(PythonPackage):
    """PyYAML is a YAML parser and emitter for Python."""
    homepage = "http://pyyaml.org/wiki/PyYAML"
    url      = "http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz"

    version('3.12', '4c129761b661d181ebf7ff4eb2d79950')
    version('3.11', 'f50e08ef0fe55178479d3a618efe21db')
