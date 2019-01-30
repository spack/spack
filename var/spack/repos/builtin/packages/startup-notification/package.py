# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class StartupNotification(AutotoolsPackage):
    """startup-notification contains a reference implementation of the
    freedesktop startup notification protocol."""

    homepage = "https://www.freedesktop.org/wiki/Software/startup-notification/"
    url      = "http://www.freedesktop.org/software/startup-notification/releases/startup-notification-0.12.tar.gz"

    version('0.12', '2cd77326d4dcaed9a5a23a1232fb38e9')

    depends_on('libx11')
    depends_on('libxcb')
    depends_on('xcb-util')
