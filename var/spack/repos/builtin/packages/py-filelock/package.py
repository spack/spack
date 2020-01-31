# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFilelock(PythonPackage):
    """This package contains a single module, which implements a platform
    independent file lock in Python, which provides a simple way of
    inter-process communication"""

    homepage = "https://github.com/benediktschmitt/py-filelock"
    url = "https://github.com/benediktschmitt/py-filelock/archive/v3.0.4.tar.gz"

    version('3.0.4',  sha256='8521523f3eafb7bbbdd0a5a7a15ddb8076ea6f106385bbfc4c9d055db2585214')
    version('3.0.3',  sha256='8e1b1ad91de70e091de381ab8705b37e41d240c211d8d888dcf1d0e31d6274bb')
    version('3.0.1',  sha256='533107ab60de691030b7e90105ab38c8b0d60d52de382fe5302819cba95561f8')
    version('3.0.0',  sha256='f41bed24b280b2fd11b2f12fecdfd2a21e5f9babc4e89929b316946288fa195c')
    version('2.0.13', sha256='85e2a001693c2995854e42783a8c11994d143f8ba9c92d31f573476a22a5b3b3')
    version('2.0.12', sha256='3b67cddd8c405c27b9118a1383d5257b5b6e066d3a9a30ab03d42b4dc6828cbb')
    version('2.0.11', sha256='97c36de6e0c2eaed6638a9575a96d176e4ec2820b888f3da3194bbb852f86c5e')
    version('2.0.10', sha256='f15d99cfa3e89072d7709bf3b5d354cf1c9096cffdb1127c4dbff1ca4a89cb84')
    version('2.0.9',  sha256='86d8e95afe77bc92a94c2e0db2b452c067b453b017fd78edfbb679b199dadbd5')
    version('2.0.8',  sha256='4f69474338ebf6ead2e0c2e91c5f94a25af8125d307f539db10886a19e2e2628')
