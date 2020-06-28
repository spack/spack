# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jql(CargoPackage):
    """A JSON Query Language CLI tool built with Rust"""

    homepage = "https://github.com/yamafaktory/jql"
    crates_io = "jql"
    git = "https://github.com/yamafaktory/jql.git"

    maintainers = ['AndrewGaspar']

    # jql doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    version('master', branch='master')
    version('2.6.1', sha256='849810db82ae770c9e9c64ee5a739ef624b67cf5e37ae806ce62fccee0cb8220')
