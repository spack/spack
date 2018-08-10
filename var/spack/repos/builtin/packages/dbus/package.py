##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Dbus(Package):
    """D-Bus is a message bus system, a simple way for applications to
       talk to one another. D-Bus supplies both a system daemon (for
       events such new hardware device printer queue ) and a
       per-user-login-session daemon (for general IPC needs among user
       applications). Also, the message bus is built on top of a
       general one-to-one message passing framework, which can be used
       by any two applications to communicate directly (without going
       through the message bus daemon)."""

    homepage = "http://dbus.freedesktop.org/"
    url      = "http://dbus.freedesktop.org/releases/dbus/dbus-1.8.8.tar.gz"

    version('1.12.8', '2764bf150e5aa8005b7bc0d6c388756a')
    version('1.11.2', '957a07f066f3730d2bb3ea0932f0081b')
    version('1.9.0', 'ec6895a4d5c0637b01f0d0e7689e2b36')
    version('1.8.8', 'b9f4a18ee3faa1e07c04aa1d83239c43')
    version('1.8.6', '6a08ba555d340e9dfe2d623b83c0eea8')
    version('1.8.4', '4717cb8ab5b80978fcadf2b4f2f72e1b')
    version('1.8.2', 'd6f709bbec0a022a1847c7caec9d6068')

    depends_on('expat')

    def install(self, spec, prefix):
        configure(
            "--prefix=%s" % prefix,
            "--disable-systemd",
            "--disable-launchd")
        make()
        make("install")

        # dbus needs a machine id generated after install
        dbus_uuidgen = Executable(join_path(prefix.bin, 'dbus-uuidgen'))
        dbus_uuidgen('--ensure')
