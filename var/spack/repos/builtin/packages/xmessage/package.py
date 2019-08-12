# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xmessage(AutotoolsPackage):
    """xmessage displays a message or query in a window.  The user can click
    on an "okay" button to dismiss it or can select one of several buttons
    to answer a question.  xmessage can also exit after a specified time."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xmessage"
    url      = "https://www.x.org/archive/individual/app/xmessage-1.0.4.tar.gz"

    version('1.0.4', '69df5761fbec14c782948065a6f36028')

    depends_on('libxaw')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
