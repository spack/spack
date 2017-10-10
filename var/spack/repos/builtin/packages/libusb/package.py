##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Libusb(AutotoolsPackage):
    """libusb is a C library that provides generic access to USB devices. It
    is intended to be used by developers to facilitate the production of
    applications that communicate with USB hardware.

    It is portable: Using a single cross-platform API, it provides access to
    USB devices on Linux, OS X, Windows, Android, OpenBSD, etc.

    It is user-mode: No special privilege or elevation is required for the
    application to communicate with a device.

    It is version-agnostic: All versions of the USB protocol, from 1.0 to 3.1
    (latest), are supported.
    """

    homepage = "http://libusb.info/"
    url      = "https://downloads.sourceforge.net/project/libusb/libusb-1.0/libusb-1.0.21/libusb-1.0.21.tar.bz2"

    version('1.0.21', '1da9ea3c27b3858fa85c5f4466003e44')

    depends_on("m4", type="build")

    # NOTE: this package probably works on all Linux, likely OSX
    #       *as-is*.  There are far too many options for me to understand.
    #
    #       The package likely does not work on Windows.  If you need that
    #       refer to WIN_INSTALL on their GitHub page.

    # NOTE: this package *RELIES* on libudev, which requires the systemd PR
    #       to be fixed.  So as it stands, users must ensure that they have
    #       libudev headers and library.  On Fedora, this was available via
    #       dnf install systemd systemd-devel systemd-libs
    #       the apt repos should be similarly named (apt-cache search systemd)
