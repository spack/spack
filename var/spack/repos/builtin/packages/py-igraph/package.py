# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIgraph(PythonPackage):
    """igraph is a collection of network analysis tools with the emphasis on
       efficiency, portability and ease of use."""

    homepage = "http://igraph.org/"
    url      = "http://igraph.org/nightly/get/python/python-igraph-0.7.0.tar.gz"

    version('0.7.0', '32a3238cb9041b1686d7d0ba152235bf')

    depends_on('py-setuptools', type='build')
    depends_on('igraph')
