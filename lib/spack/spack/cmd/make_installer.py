# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import os
import posixpath
import sys

import spack.concretize
import spack.paths
import spack.util.executable
from spack.llnl.path import convert_to_posix_path

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
    with open(file_path, "r+", encoding="utf-8") as f:
        for line in f.readlines():
            contents += line_to_rtf(line)
    return rtf_header.format(contents)


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    spack_source_group = subparser.add_mutually_exclusive_group(required=True)
    spack_source_group.add_argument(
        "-v", "--spack-version", default="", help="download given spack version"
    )
    spack_source_group.add_argument(
        "-s", "--spack-source", default="", help="full path to spack source"
    )

    subparser.add_argument(
        "-g",
        "--git-installer-verbosity",
        default="",
        choices=["SILENT", "VERYSILENT"],
        help="level of verbosity provided by bundled git installer (default is fully verbose)",
        required=False,
        action="store",
        dest="git_verbosity",
    )

    subparser.add_argument("output_dir", help="output directory")


def make_installer(parser, args):
    """
    Use CMake to generate WIX installer in newly created build directory
    """
    if sys.platform == "win32":
        output_dir = args.output_dir
        cmake_spec = spack.concretize.concretize_one("cmake")
        cmake_path = os.path.join(cmake_spec.prefix, "bin", "cmake.exe")
        cpack_path = os.path.join(cmake_spec.prefix, "bin", "cpack.exe")
        spack_source = args.spack_source
        git_verbosity = ""
        if args.git_verbosity:
            git_verbosity = "/" + args.git_verbosity

        if spack_source:
            if not os.path.exists(spack_source):
                print(f"{spack_source} does not exist")
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

        with open(spack_license, "w", encoding="utf-8") as rtf_license:
            written = rtf_license.write(rtf_spack_license)
            if written == 0:
                raise RuntimeError("Failed to generate properly formatted license file")
        spack_logo = posixpath.join(posix_root, "share/spack/logo/favicon.ico")

        try:
            spack.util.executable.Executable(cmake_path)(
                "-S",
                source_dir,
                "-B",
                output_dir,
                f"-DSPACK_VERSION={spack_version}",
                f"-DSPACK_SOURCE={spack_source}",
                f"-DSPACK_LICENSE={spack_license}",
                f"-DSPACK_LOGO={spack_logo}",
                f"-DSPACK_GIT_VERBOSITY={git_verbosity}",
            )
        except spack.util.executable.ProcessError:
            print("Failed to generate installer")
            return spack.util.executable.ProcessError.returncode

        try:
            spack.util.executable.Executable(cpack_path)(
                "--config", f"{output_dir}/CPackConfig.cmake", "-B", f"{output_dir}/"
            )
        except spack.util.executable.ProcessError:
            print("Failed to generate installer")
            return spack.util.executable.ProcessError.returncode
        try:
            spack.util.executable.Executable(os.environ.get("WIX") + "/bin/candle.exe")(
                "-ext",
                "WixBalExtension",
                f"{output_dir}/bundle.wxs",
                "-out",
                f"{output_dir}/bundle.wixobj",
            )
        except spack.util.executable.ProcessError:
            print("Failed to generate installer chain")
            return spack.util.executable.ProcessError.returncode
        try:
            spack.util.executable.Executable(os.environ.get("WIX") + "/bin/light.exe")(
                "-sw1134",
                "-ext",
                "WixBalExtension",
                f"{output_dir}/bundle.wixobj",
                "-out",
                f"{output_dir}/Spack.exe",
            )
        except spack.util.executable.ProcessError:
            print("Failed to generate installer chain")
            return spack.util.executable.ProcessError.returncode
        print(f"Successfully generated Spack.exe in {output_dir}")
    else:
        print("The make-installer command is currently only supported on Windows.")
