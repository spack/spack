# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySmartOpen(PythonPackage):
    """smart_open is a Python 2 & Python 3 library for efficient streaming of
       very large files from/to S3, HDFS, WebHDFS, HTTP, or local storage. It
       supports transparent, on-the-fly (de-)compression for a variety of
       different formats."""

    homepage = "https://github.com/piskvorky/smart_open"
    url      = "https://github.com/RaRe-Technologies/smart_open/archive/1.8.4.tar.gz"

    version('1.8.4', sha256='788e07f035defcbb62e3c1e313329a70b0976f4f65406ee767db73ad5d2d04f9')

    depends_on('py-setuptools', type='build')
    depends_on('py-boto3', type=('build', 'run'))
