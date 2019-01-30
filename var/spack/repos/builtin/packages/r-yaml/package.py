# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYaml(RPackage):
    """This package implements the libyaml YAML 1.1 parser and emitter
    (http://pyyaml.org/wiki/LibYAML) for R."""

    homepage = "https://cran.r-project.org/web/packages/yaml/index.html"
    url      = "https://cran.r-project.org/src/contrib/yaml_2.1.13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/yaml"

    version('2.1.14', '2de63248e6a122c368f8e4537426e35c')
    version('2.1.13', 'f2203ea395adaff6bd09134666191d9a')
