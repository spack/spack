# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYaml(RPackage):
    """This package implements the libyaml YAML 1.1 parser and emitter
    (http://pyyaml.org/wiki/LibYAML) for R."""

    homepage = "https://cloud.r-project.org/package=yaml"
    url      = "https://cloud.r-project.org/src/contrib/yaml_2.1.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/yaml"

    version('2.2.0', sha256='55bcac87eca360ab5904914fcff473a6981a1f5e6d2215d2634344d0ac30c546')
    version('2.1.19', sha256='e5db035693ac765e4b5fe1fc2e9711f8ca73e398e3f2bf27cc60def59ccd7f11')
    version('2.1.14', '2de63248e6a122c368f8e4537426e35c')
    version('2.1.13', 'f2203ea395adaff6bd09134666191d9a')
