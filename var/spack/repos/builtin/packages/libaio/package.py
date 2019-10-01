# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Libaio(Package):
    """This is the linux native Asynchronous I/O interface library."""

    homepage = "http://lse.sourceforge.net/io/aio.html"
    url = "https://debian.inf.tu-dresden.de/debian/pool/main/liba/libaio/libaio_0.3.110.orig.tar.gz"

    version('0.3.110', '2a35602e43778383e2f4907a4ca39ab8')

    conflicts('platform=darwin', msg="libaio is a linux specific library")

    def install(self, spec, prefix):
        make('prefix={0}'.format(prefix), 'install')
