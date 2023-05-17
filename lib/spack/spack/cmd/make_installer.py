# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import posixpath
import sys

from llnl.util import tty

import spack.paths
import spack.util.executable
from spack.spec import Spec
from spack.util.path import convert_to_posix_path

description = "generate Windows installer"
section = "admin"
level = "long"


def txt_to_rtf(file_path):
    rtf_header = r"""{{\rtf1\ansi\deff0\nouicompat
    {{\fonttbl{{\f0\\fnil\fcharset0 Courier New;}}}}
    {{\colortbl ;\red0\green0\blue255;}}
    {{\*\generator Riched20 10.0.19041}}\viewkind4\uc1
    \f0\fs22\lang1033
    {}
    }}
    """

    def line_to_rtf(str):
        return str.replace("\n", "\\par")

    contents = ""
    with open(file_path, "r+") as f:
        for line in f.readlines():
            contents += line_to_rtf(line)
    return rtf_header.format(contents)


def setup_parser(subparser):
    spack_source_group = subparser.add_mutually_exclusive_group(required=True)
    spack_source_group.add_argument(
        "-v", "--spack-version", default="", help="download given spack version e.g. 0.16.0"
    )
    spack_source_group.add_argument(
        "-s", "--spack-source", default="", help="full path to spack source"
    )

    subparser.add_argument(
        "-g",
        "--git-installer-verbosity",
        default="",
        choices=set(["SILENT", "VERYSILENT"]),
        help="Level of verbosity provided by bundled Git Installer.\
             Default is fully verbose",
        required=False,
        action="store",
        dest="git_verbosity",
    )
    subparser.add_argument(
        "-a",
        "--arch",
        default="64",
        choices=["64", "32"],
        help="Architecture targeted by bundled Git/Python"
    )
    python_version_group = subparser.add_argument_group("Python version and hash", required=False)
    python_version_group.add_argument("-pv", "--python-version", default="", help="Python version to be bundled with installer")
    python_version_group.add_argument("-ph", "--python-hash", default="", help="Python distribution hash for associated version, must be provided if --python-version is specified")

    git_version_group = subparser.add_argument_group("Git version and hash", required=False)
    git_version_group.add_argument("-gv", "--git-version", default="", help="Git version to be bundled with installer" )
    git_version_group.add_argument("-gh", "--git-hash", default="", help="Git installer hash for associated version, must be provided if --git-version is specified")

    subparser.add_argument("output_dir", help="output directory")


def make_installer(parser, args):
    """
    Use CMake to generate WIX installer in newly created build directory
    """
    if sys.platform == "win32":
        git_version = args.git_version
        python_version = args.python_version
        if git_version and not args.git_hash:
            parser.error("Git version specified without hash"
                         "\nPlease specify sha256 hash for installer if specifying Git version")
        git_hash = args.git_hash
        if python_version and not args.python_hash:
            parser.error("Python version specified without hash"
                         "\nPlease specify sha256 hash for distribution if specifying Python version")
        python_hash = args.python_hash
        output_dir = args.output_dir
        cmake_spec = Spec("cmake")
        cmake_spec.concretize()
        if not (cmake_spec.installed or cmake_spec.external):
            # Spack is not aware of a CMake, fallback on one being present in PATH
            # but warn user it may not be available.
            cmake_path = "cmake.exe"
            cpack_path = "cpack.exe"
            tty.warn(
                "Spack is not aware of a CMake installation. Defaulting to what is available on the PATH to create the installer"
                "\nYou may want to consider installing or externally detecting via Spack for better results."
            )
        else:
            cmake_path = os.path.join(cmake_spec.prefix, "bin", "cmake.exe")
            cpack_path = os.path.join(cmake_spec.prefix, "bin", "cpack.exe")

        spack_source = args.spack_source
        git_verbosity = ""
        if args.git_verbosity:
            git_verbosity = "/" + args.git_verbosity

        if spack_source:
            if not os.path.exists(spack_source):
                print("%s does not exist" % spack_source)
                return
            else:
                if not os.path.isabs(spack_source):
                    spack_source = posixpath.abspath(spack_source)
                spack_source = convert_to_posix_path(spack_source)

        spack_version = args.spack_version

        here = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(here, "installer")
        posix_root = convert_to_posix_path(spack.paths.spack_root)
        spack_license = posixpath.join(posix_root, "LICENSE-APACHE")
        rtf_spack_license = txt_to_rtf(spack_license)
        spack_license = posixpath.join(source_dir, "LICENSE.rtf")

        with open(spack_license, "w") as rtf_license:
            written = rtf_license.write(rtf_spack_license)
            if written == 0:
                raise RuntimeError("Failed to generate properly formatted license file")
        spack_logo = posixpath.join(posix_root, "share/spack/logo/favicon.ico")

        cmake_args = [
            "-S",
            source_dir,
            "-B",
            output_dir,
            "-DSPACK_VERSION=%s" % spack_version,
            "-DSPACK_SOURCE=%s" % spack_source,
            "-DSPACK_LICENSE=%s" % spack_license,
            "-DSPACK_LOGO=%s" % spack_logo,
            "-DSPACK_GIT_VERBOSITY=%s" % git_verbosity,
            "-DARCH=%s" % args.arch
        ]
        if python_version:
            cmake_args.extend([
                "-DPYTHON_VERSION=%s" % python_version,
                "-DPYTHON_HASH=%s" % python_hash,
            ])
        if git_version:
            cmake_args.extend([
                "-DGIT_VERSION=%s" % git_version,
                "-DGIT_HASH=%s" % git_hash
            ])

        try:
            spack.util.executable.Executable(cmake_path)(
                *cmake_args
            )
        except spack.util.executable.ProcessError as pe:
            tty.error("Failed to generate installer")
            raise pe

        try:
            spack.util.executable.Executable(cpack_path)(
                "--config", "%s/CPackConfig.cmake" % output_dir, "-B", "%s/" % output_dir
            )
        except spack.util.executable.ProcessError as pe:
            tty.error("Failed to generate installer")
            raise pe
        try:
            spack.util.executable.Executable(os.environ.get("WIX") + "/bin/candle.exe")(
                "-ext",
                "WixBalExtension",
                "%s/bundle.wxs" % output_dir,
                "-out",
                "%s/bundle.wixobj" % output_dir,
            )
        except spack.util.executable.ProcessError as pe:
            tty.error("Failed to generate installer chain")
            raise pe
        try:
            spack.util.executable.Executable(os.environ.get("WIX") + "/bin/light.exe")(
                "-sw1134",
                "-ext",
                "WixBalExtension",
                "%s/bundle.wixobj" % output_dir,
                "-out",
                "%s/Spack.exe" % output_dir,
            )
        except spack.util.executable.ProcessError as pe:
            tty.error("Failed to generate installer chain")
            raise pe
        tty.info("Successfully generated Spack.exe in %s" % (output_dir))
    else:
        tty.error("The make-installer command is currently only supported on Windows.")
