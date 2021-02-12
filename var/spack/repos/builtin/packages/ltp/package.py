# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ltp(AutotoolsPackage):
    """Ltp is a joint project started by SGI, developed and maintained by IBM,
    Cisco, Fujitsu, SUSE, Red Hat and others, that has a goal to deliver
    test suites to the open source community that validate the reliability,
    robustness,and stability of Linux. The LTP testsuite contains a collection
    of tools for testing the Linux kernel and related features."""

    homepage = "https://github.com/linux-test-project/ltp"
    url      = "https://github.com/linux-test-project/ltp/archive/20190517.tar.gz"

    version('20210121', sha256='c6f944e5b873eda51d1ede00a170058b20c67dd1c128f59b39b8174485881478')
    version('20200930', sha256='12696d9a3a967daa94cccd2c05b65b4c185eb4ec290fa6b76bf32d0ff2427a43')
    version('20200515', sha256='d2c96d77ea80d3bb8ae3da76c96de9c352c439a74a069afa29b7475293944791')
    version('20200120', sha256='414fdf153ca56c7342d721cd70498f979a30f8b70f58eb9336b5ae12ca30f70e')
    version('20190930', sha256='eca11dbe11a61f3035561a2aa272d578ca9380563440f9ba876c0c4755a42533')
    version('20190517', sha256='538175fff2d6c9d69748b2d4afcf5ac43f7300456f839fa7b5b101c7ad447af7')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
