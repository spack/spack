# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpMessage(PerlPackage):
    """HTTP style message (base class)"""

    homepage = "http://search.cpan.org/~oalders/HTTP-Message-6.13/lib/HTTP/Status.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Message-6.13.tar.gz"

    version('6.27', sha256='0be0f720fbbbdbae8711f6eec9b2f0d34bd5ed5046fc66b80dc3b42017c1e699')
    version('6.26', sha256='6ce6c359de75c3bb86696a390189b485ec93e3ffc55326b6d044fa900f1725e1')
    version('6.24', sha256='554a1acf2daa401091f7012f5cb82d04d281db43fbd8f39a1fcbb7ed56dde16d')
    version('6.22', sha256='970efd151b81c95831d2a5f9e117f8032b63a1768cd2cd3f092ad634c85175c3')
    version('6.18', sha256='d060d170d388b694c58c14f4d13ed908a2807f0e581146cef45726641d809112')
    version('6.17', sha256='b0ba6cadff95367dfc97eaf63eea95cd795eeacf61f7bcdfa169127e015c6984')
    version('6.16', sha256='46790ae127946d5cfea5a1e05c1b9f4a045a7c5094fe81f086bbf3341290ebd0')
    version('6.15', sha256='7b244a193b6ffb9728a4cb25a09bc7c938956baa2ee1983ee2cbc4ed75dccb85')
    version('6.14', sha256='71aab9f10eb4b8ec6e8e3a85fc5acb46ba04db1c93eb99613b184078c5cf2ac9')
    version('6.13', sha256='f25f38428de851e5661e72f124476494852eb30812358b07f1c3a289f6f5eded')

    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-encode-locale', type=('build', 'run'))
    depends_on('perl-io-html', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
