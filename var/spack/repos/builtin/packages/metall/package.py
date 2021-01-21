# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"
    url      = "https://github.com/LLNL/metall/archive/v0.2.tar.gz"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('master', branch='master')
    version('develop', branch='develop')

    version('0.9', sha256='2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927')
    version('0.8', sha256='02d7379a499ecd6ff7a3aaae436a2cd4dbe21c2fc23f5dad7449e7e8c832c77b')
    version('0.7', sha256='17430758a0d2821d1220b03c2635f44739400bad1ffe308fd3da6e38ae875ced')
    version('0.6', sha256='123234c7214b666ed51db255c3e2acf98c2cd91bdf1cd0a254bdb893c2148afa')
    version('0.5', sha256='7d710dc3d5270c799d3506566e5c3c45b94d6f87fb5e05bbaecdca04e42f2966')
    version('0.4', sha256='6309dab9cffba3bfc957f23e5a287de00966237baafea759866b2961d8db34ea')
    version('0.3', sha256='abecdd245eae69088e001cc0c641e8f560b554a726a515eebd7b7f7fb43361e5')
    version('0.2', sha256='35cdf3505d2f8d0282a0d5c60b69a0ec5ec6d77ac3facce7549eb874df27be1d')

    depends_on('boost@1.64:', type=('build', 'link'))

    def cmake_args(self):
        args = []
        args.append('-DINSTALL_HEADER_ONLY=ON')
        return args
