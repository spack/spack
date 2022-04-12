# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lwtnn(CMakePackage):
    """Lightweight Trained Neural Network."""

    homepage = "https://github.com/lwtnn/lwtnn"
    url      = "https://github.com/lwtnn/lwtnn/archive/refs/tags/v2.12.1.tar.gz"

    maintainers = ['haralmha']

    version('2.12.1', sha256='b820e698d4ed60737e646ca87a42354e8ac548403348b7f2940e8fda1c0f8203')
    version('2.10', sha256='bf84b290c44da582226344b0d5febf7fdbd1cbdee94fcc8bcac972c7355564ed')

    depends_on('boost@1.54:')
    depends_on('eigen@:3.3.99', when='@2.11:')
    depends_on('eigen')
