# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XorgCfFiles(AutotoolsPackage):
    """The xorg-cf-files package contains the data files for the imake utility,
    defining the known settings for a wide variety of platforms (many of which
    have not been verified or tested in over a decade), and for many of the
    libraries formerly delivered in the X.Org monolithic releases."""

    homepage = "http://cgit.freedesktop.org/xorg/util/cf"
    url      = "https://www.x.org/archive/individual/util/xorg-cf-files-1.0.6.tar.gz"

    version('1.0.6', 'c0ce98377c70d95fb48e1bd856109bf8')

    depends_on('pkgconfig', type='build')
