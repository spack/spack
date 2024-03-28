# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyZipstreamNew(PythonPackage):
    """Zipfile generator that takes input files as well as streams"""

    homepage = "https://github.com/arjan-s/python-zipstream"
    pypi = "zipstream-new/zipstream-new-1.1.8.tar.gz"

    version(
        "1.1.8",
        sha256="0662eb3ebe764fa168a5883cd8819ef83b94bd9e39955537188459d2264a7f60",
        url="https://pypi.org/packages/81/f3/d7b4c8c9b6657ff0db27b739894ed0665fa8f3c78a7452bf74d6447f6865/zipstream_new-1.1.8-py3-none-any.whl",
    )
