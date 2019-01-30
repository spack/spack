# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMx(PythonPackage):
    """The eGenix.com mx Base Distribution for Python is a collection of
       professional quality software tools which enhance Python's
       usability in many important areas such as fast text searching,
       date/time processing and high speed data types.

    """
    homepage = "http://www.egenix.com/products/python/mxBase/"
    url      = "https://downloads.egenix.com/python/egenix-mx-base-3.2.8.tar.gz"

    version('3.2.8', '9d9d3a25f9dc051a15e97f452413423b')
