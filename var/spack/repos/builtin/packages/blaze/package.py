# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Blaze(CMakePackage):
    """Blaze is an open-source, high-performance C++ math library for dense and
    sparse arithmetic. With its state-of-the-art Smart Expression Template
    implementation Blaze combines the elegance and ease of use of a
    domain-specific language with HPC-grade performance, making it one of the
    most intuitive and fastest C++ math libraries available.
    """

    homepage = "https://bitbucket.org/blaze-lib/blaze/overview"
    url      = "https://bitbucket.org/blaze-lib/blaze/downloads/blaze-3.5.tar.gz"
    git      = "https://bitbucket.org/blaze-lib/blaze.git"

    # Blaze requires at least cmake 3.8.0 for C++14 features.
    depends_on('cmake@3.8.0:', type='build')

    version('master', branch='master')
    version('3.5', sha256='f50d4a57796b8012d3e6d416667d9abe6f4d95994eb9deb86cd4491381dec624')
    version('3.4', sha256='fd474ab479e81d31edf27d4a529706b418f874caa7b046c67489128c20dda66f')
    version('3.3', sha256='138cbb7b95775c10bf56a5ab3596a32205751299b19699984b6ed55b1bf989d0')
    version('3.2', '47bd4a4f1b6292f5a6f71ed9d5287480')
    version('3.1', '2938e015f0d274e8d62ee5c4c0c1e9f3')
    version('3.0', '0c4cefb0be7b5a27ed8a377941be1ab1')
    version('2.6', 'f7b515eeffd5cce92eb02dc6f8905f4d')
    version('2.5', '53a862763c275046ff0a8f07dfd3985b')
    version('2.4', '7cf2e963a73d3c95ced0f7eaa0ae3677')
    version('2.3', '2f8ca52d23447ac75a03bb43b12ef774')
    version('2.2', '686a514108d7f3c6c7325ed57c171a59')
    version('2.1', 'e5e419a2b35f0a36cd9d7527a250c56a')
    version('2.0', 'aeb6a865e9e3810ee55456f961458a8e')
    version('1.5', '5b77b605ee5ad35631bb3039737142c9')
    version('1.4', '3f06d710161954ccae0975d87f1069ca')
    version('1.3', 'ebd7f91fc5fca4108bfd16a86f9abd82')
    version('1.2', 'b1511324456c3f70fce198a2b63e71ef')
    version('1.1', '5e52ebe68217f2e50d66dfdb9803d51e')
    version('1.0', 'a46508a2965ace9d89ded30a386d9548')
