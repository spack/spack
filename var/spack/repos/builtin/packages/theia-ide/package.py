# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TheiaIde(Package):
    """A modern and open IDE for cloud and desktop.
    The Theia IDE is based on the Theia platform."""

    homepage = "https://theia-ide.org/"
    url = "https://github.com/eclipse-theia/theia-ide/archive/refs/tags/v1.59.1.tar.gz"

    maintainers("RobertMaaskant")

    license("MIT", checked_by="RobertMaaskant")

    version("1.59.1", sha256="f3e4fdb76aa0d5a4f034d9fe8889e8c798425d8c0a452688277002b7f09ea7d0")

    conflicts("platform=darwin", msg="Currently only packaged for Linux")
    conflicts("platform=windows", msg="Currently only packaged for Linux")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with default_args(type="build"):
        depends_on("gmake")
        depends_on("kbproto")
        depends_on("libsecret")
        depends_on("libx11")
        depends_on("libxau")
        depends_on("libxcb")
        depends_on("libxdmcp")
        depends_on("libxkbfile")
        depends_on("pkg-config")
        depends_on("xproto")

        depends_on("npm@10.8.2:")
        depends_on("yarn@1.7.0:1")

        # required by node-gyp ^9.0.0: https://github.com/eclipse-theia/theia/blob/v1.59.0/package.json#L45
        # https://github.com/nodejs/node-gyp/tree/v9.0.0?tab=readme-ov-file#on-unix
        depends_on("python@3.7:3.10")

    with default_args(type="run"):
        depends_on("git@2.11.0:")
        # https://github.com/microsoft/vscode/blob/1.98.2/.nvmrc
        depends_on("node-js@20.18.2:20")

    def install(self, spec, prefix):
        yarn = which("yarn", required=True)
        yarn()
        yarn("build")
        yarn("download:plugins")
        yarn("package:applications")

        mkdirp(prefix.bin)
        install("applications/electron/dist/TheiaIDE.AppImage", prefix.bin.join("theia-ide"))
