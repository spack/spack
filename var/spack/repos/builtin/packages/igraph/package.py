# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Igraph(AutotoolsPackage):
    """igraph is a library for creating and manipulating graphs."""

    homepage = "http://igraph.org/"
    url      = "https://github.com/igraph/igraph/releases/download/0.7.1/igraph-0.7.1.tar.gz"

    version('0.7.1', '4f6e7c16b45fce8ed423516a9786e4e8')

    depends_on('libxml2')
