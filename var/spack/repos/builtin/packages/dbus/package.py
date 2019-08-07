# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    depends_on('pkgconfig', type='build')
    depends_on('expat')
    depends_on('glib')

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
