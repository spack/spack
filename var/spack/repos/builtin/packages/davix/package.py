# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Davix(CMakePackage):
    """High-performance file management over WebDAV/HTTP."""

    homepage = "https://dmc.web.cern.ch/projects/davix"
    url      = "http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/davix/0.6.7/davix-0.6.7.tar.gz"
    list_url = "http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/davix/"
    list_depth = 1

    version('0.6.8', 'e1820f4cc3fc44858ae97197a3922cce2a1130ff553b080ba19e06eb8383ddf7',
            url='http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/davix/0.6.8/davix-0.6.8.tar.gz')

    depends_on('pkgconfig', type='build')
    depends_on('libxml2')
    depends_on('libuuid')
    depends_on('openssl')
