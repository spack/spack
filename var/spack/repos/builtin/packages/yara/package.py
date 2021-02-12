# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Yara(AutotoolsPackage):
    """YARA is a tool aimed at (but not limited to) helping malware researchers
    to identify and classify malware samples"""

    homepage = "http://virustotal.github.io/yara/"
    url      = "https://github.com/VirusTotal/yara/archive/v3.9.0.tar.gz"

    version('4.0.5',  sha256='ea7ebefad05831faf6f780cab721611b0135803f03a84c27eeba7bfe0afc3aae')
    version('4.0.4',  sha256='67fdc6f1050261914cf4a9e379b60961f62c2f76af676bafb2ceb47dd642d44f')
    version('4.0.3',  sha256='d95b7f5e2981328a10ea206e3384d661bd4d488e43e8d1785152bdea44d89880')
    version('4.0.2',  sha256='05ad88eac9a9f0232432fd14516bdaeda14349d6cf0cac802d76e369abcee001')
    version('4.0.1',  sha256='c63e2c4d73fc37e860db5d7e13d945684a0a6d1d17be7161fe1dd8f99268b03c')
    version('4.0.0',  sha256='8ee411fe3a60d1b463f152e356e0ee46b23331c461fd60ef8f82fed580c73f46')
    version('3.11.0', sha256='de8c54028c848751c06f5acc3b749c3ef6b111090b39f6ff991295af44bd4633')
    version('3.9.0', sha256='ebe7fab0abadb90449a62afbd24e196e18b177efe71ffd8bf22df95c5386f64d')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
