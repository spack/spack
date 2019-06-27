# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyaml(PythonPackage):
    """PyYAML-based module to produce pretty and readable YAML-serialized data."""

    homepage = "https://github.com/mk-fg/pretty-yaml"
    url      = "https://pypi.io/packages/source/p/pyaml/pyaml-19.4.1.tar.gz"

    version('19.4.1', 'b6491ffe4ce2af98e94d23808cfa234d')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-pyyaml', type='run')
