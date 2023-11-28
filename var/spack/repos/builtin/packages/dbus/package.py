# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbus(AutotoolsPackage):
    """D-Bus is a message bus system, a simple way for applications to
    talk to one another. D-Bus supplies both a system daemon (for
    events such new hardware device printer queue ) and a
    per-user-login-session daemon (for general IPC needs among user
    applications). Also, the message bus is built on top of a
    general one-to-one message passing framework, which can be used
    by any two applications to communicate directly (without going
    through the message bus daemon)."""

    homepage = "https://dbus.freedesktop.org/"
    url = "https://dbus.freedesktop.org/releases/dbus/dbus-1.8.8.tar.gz"

    version("1.13.6", sha256="b533693232d36d608a09f70c15440c1816319bac3055433300d88019166c1ae4")
    version("1.12.8", sha256="e2dc99e7338303393b6663a98320aba6a63421bcdaaf571c8022f815e5896eb3")
    version("1.11.2", sha256="5abc4c57686fa82669ad0039830788f9b03fdc4fff487f0ccf6c9d56ba2645c9")
    version("1.9.0", sha256="38ebc695b5cbbd239e0f149aa5d5395f0051a0fec1b74f21ff2921b22a31c171")
    version("1.8.8", sha256="dfab263649a979d0fff64a30cac374891a8e9940350e41f3bbd7679af32bd1fd")
    version("1.8.6", sha256="eded83ca007b719f32761e60fd8b9ffd0f5796a4caf455b01b5a5ef740ebd23f")
    version("1.8.4", sha256="3ef63dc8d0111042071ee7f7bafa0650c6ce2d7be957ef0b7ec269495a651ff8")
    version("1.8.2", sha256="5689f7411165adc953f37974e276a3028db94447c76e8dd92efe910c6d3bae08")

    variant("xml_docs", default=False, description="Build XML documentation")
    variant("system-socket", default="default", description="Location for the DBus system socket")

    depends_on("pkgconfig", type="build")
    depends_on("docbook-xml", type="build")
    depends_on("docbook-xsl", type="build")
    depends_on("expat")
    depends_on("glib")
    depends_on("libsm")
    depends_on("xmlto", when="+xml_docs", type="build")

    def configure_args(self):
        args = ["--disable-systemd", "--disable-launchd"]
        args += self.enable_or_disable("xml-docs", variant="xml_docs")
        socket = self.spec.variants["system-socket"].value
        if socket != "default":
            args += ["--with-system-socket={0}".format(socket)]
        return args

    @run_after("install")
    def generate_uuid(self):
        # dbus needs a machine id generated after install
        dbus_uuidgen = Executable(self.prefix.bin.join("dbus-uuidgen"))
        dbus_uuidgen("--ensure")
