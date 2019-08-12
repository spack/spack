# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apr(AutotoolsPackage):
    """Apache portable runtime."""

    homepage  = 'https://apr.apache.org/'
    url       = 'http://archive.apache.org/dist/apr/apr-1.6.2.tar.gz'

    version('1.6.2', '8672e78514e3fcef2643127c524bf0f9')
    version('1.5.2', '98492e965963f852ab29f9e61b2ad700')
