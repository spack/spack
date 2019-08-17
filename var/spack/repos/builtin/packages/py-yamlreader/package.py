# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYamlreader(PythonPackage):
    """Yamlreader merges YAML data from a directory, a list of files or a
    file glob."""

    homepage = "http://pyyaml.org/wiki/PyYAML"
    url      = "https://pypi.io/packages/source/y/yamlreader/yamlreader-3.0.4.tar.gz"

    version('3.0.4', '542179b5b5bedae941245b8b673119db')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
