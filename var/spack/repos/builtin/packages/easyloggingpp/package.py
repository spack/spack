# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Easyloggingpp(CMakePackage):
    """Single header C++ logging library"""

    homepage = "https://github.com/zuhd-org/easyloggingpp"
    url      = "https://github.com/zuhd-org/easyloggingpp/archive/v9.96.7.tar.gz"

    version('9.96.7', sha256='237c80072b9b480a9f2942b903b4b0179f65e146e5dcc64864dc91792dedd722')
