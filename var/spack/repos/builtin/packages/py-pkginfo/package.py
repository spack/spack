# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPkginfo(PythonPackage):
    """Query metadatdata from sdists / bdists / installed packages."""

    homepage = "https://code.launchpad.net/~tseaver/pkginfo/trunk"
    pypi = "pkginfo/pkginfo-1.5.0.1.tar.gz"

    version('1.7.1', sha256='e7432f81d08adec7297633191bbf0bd47faf13cd8724c3a13250e51d542635bd')
    version('1.5.0.1', sha256='7424f2c8511c186cd5424bbf31045b77435b37a8d604990b79d4e70d741148bb')

    depends_on('py-setuptools', type=('build', 'run'))
