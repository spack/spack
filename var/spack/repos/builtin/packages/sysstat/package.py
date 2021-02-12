# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sysstat(AutotoolsPackage):
    """The sysstat package contains various utilities, common to many
    commercial Unixes, to monitor system performance and usage activity
    Sysstat also contains tools you can schedule via cron or systemd to
    collect and historize performance and activity data."""

    homepage = "https://github.com/sysstat"
    url      = "https://github.com/sysstat/sysstat/archive/v12.1.6.tar.gz"

    version('12.5.2', sha256='d879f194ba5c0c2c990c96981e483c1deae0a2003dd8341a20efc6fc07f7ba9e')
    version('12.5.1', sha256='6ebb9a98ebf28158f1cb826d13eaf6ab1d35ca79d63b922beb821de1bb13743c')
    version('12.4.2', sha256='cbfd186e79eca45082bd1b36cd99f5b6e404b7d976ed1cc8cf2f2ff482c0b710')
    version('12.4.1', sha256='728aac4b7fd1435cc85e855c11aad81f85bb8d55d9c8b6948457c53a4a4194dd')
    version('12.4.0', sha256='1962ed04832d798f5f7e787b9b4caa8b48fe935e854eef5528586b65f3cdd993')
    version('12.3.3', sha256='748944115c018dec0d3d40bedbfa1f9c5ff05404240fbff5d74ad03445c0c930')
    version('12.3.2', sha256='c53b48f0a89cf0f6ea2af67ef0caf44ceed500d37fa7042a871a0541a1ce235d')
    version('12.3.1', sha256='55c189a36ecb2eb50929588ad9bea638234cbce2d40b5f044a99fd1365f2b914')
    version('12.2.3', sha256='7979b214152724b00d4c4db1649b76dfa294fa55309a579312d3be72a6b60587')
    version('12.2.2', sha256='0d73d495eed18ab4bf77dbce6a2e94ce5276bd736906972c067b55882833e61a')
    version('12.2.0', sha256='614ab9fe8e7937a3edb7b2b6760792a3764ea3a7310ac540292dd0e3dfac86a6')
    version('12.1.7', sha256='293b31ca414915896c639a459f4d03a742b3a472953975394bef907b245b3a9f')
    version('12.1.6', sha256='50f4cbf023f8b933ed6f1fee0e6d33e508d9dc20355a47f6927e0c6046c6acf6')
    version('12.1.5', sha256='d0ea36f278fe10c7978be2a383cb8055c1277d60687ac9030ba694a08a80f6ff')
