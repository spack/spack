# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    pypi = "httpcore/httpcore-0.11.0.tar.gz"

    version('0.12.3', sha256='37ae835fb370049b2030c3290e12ed298bf1473c41bb72ca4aa78681eba9b7c9')
    version('0.12.2', sha256='dd1d762d4f7c2702149d06be2597c35fb154c5eff9789a8c5823fbcf4d2978d6')
    version('0.12.1', sha256='3c5fcd97c52c3f6a1e4d939d776458e6177b5c238b825ed51d72840e582573b5')
    version('0.12.0', sha256='2526a38f31ac5967d38b7f593b5d8c4bd3fa82c21400402f866ba3312946acbf')
    version('0.11.1', sha256='a35dddd1f4cc34ff37788337ef507c0ad0276241ece6daf663ac9e77c0b87232')
    version('0.11.0', sha256='35ffc735d746b83f8fc6d36f82600e56117b9e8adc65d0c0423264b6ebfef7bf')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-sniffio@1.0:')
    depends_on('py-h11@0.8:0.9')
