# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOdcs(PythonPackage):
    """The main goal of ODCS is to allow generation of temporary composes
    using the REST API calls"""

    homepage = "https://pagure.io/odcs"
    pypi     = "odcs/odcs-0.3.2.tar.gz"

    version('0.3.2', sha256='707d15f3123f45024d83b75a55327de2dd23cbd9f24835398e327fe123a8c990')
    version('0.3.1', sha256='a3b0672a036d6ee88c370a5467bdad24c57a1d4c0f10d6dba42c69b64958288d')
    version('0.3.0', sha256='ed3a7133786926bd87e5ab7452b86310ba7a9965e20b5400817a7e45d7da4ad5')

    depends_on('py-setuptools', type='build')
