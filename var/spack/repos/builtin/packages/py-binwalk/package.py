# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyBinwalk(PythonPackage):
    """Binwalk is a fast, easy to use tool for analyzing, reverse engineering,
       and extracting firmware images."""

    homepage = "https://github.com/devttys0/binwalk"
    url      = "https://pypi.io/packages/source/b/binwalk/binwalk-2.1.0.tar.gz"

    version('2.1.0', '054867d9abe6a05f43200cf2591051e6')

    depends_on('python')
    depends_on('py-setuptools', type='build')
