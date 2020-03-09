# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cpprestsdk(CMakePackage):
    """The C++ REST SDK is a Microsoft project for cloud-based client-server
       communication in native code using a modern asynchronous C++ API design.
       This project aims to help C++ developers connect to and interact with
       services. """

    homepage = "https://github.com/Microsoft/cpprestsdk"
    url      = "https://github.com/Microsoft/cpprestsdk/archive/v2.9.1.tar.gz"

    version('2.9.1', sha256='537358760acd782f4d2ed3a85d92247b4fc423aff9c85347dc31dbb0ab9bab16')

    depends_on('boost')

    root_cmakelists_dir = 'Release'
