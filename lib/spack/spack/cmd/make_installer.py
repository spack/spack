# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import posixpath
import subprocess
import sys

import spack.paths
import spack.util.executable
from spack.spec import Spec

description = "generate Windows installer"
section = "admin"
level = "long"


def txt_to_rtf(file_path):
    rtf_header = """{{\\rtf1\\ansi\\deff0\\nouicompat
    {{\\fonttbl{{\\f0\\fnil\\fcharset0 Courier New;}}}}
    {{\\colortbl ;\\red0\\green0\\blue255;}}
    {{\\*\\generator Riched20 10.0.19041}}\\viewkind4\\uc1
    \\f0\\fs22\\lang1033
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
        '-v', '--spack_version', default="",
        help='download given spack version e.g. 0.16.0')
    spack_source_group.add_argument(
        '-s', '--spack_source', default="",
        help='full path to spack source')

    subparser.add_argument(
        '-g', '--git-installer-verbosity', default="",
        choices=set(['SILENT', 'VERYSILENT']),
        help="Level of verbosity provided by bundled Git Installer.\
             Default is fully verbose",
        required=False, action='store', dest="git_verbosity"
    )

    subparser.add_argument(
        'output_dir', help="output directory")


def make_installer(parser, args):
    """
       Use CMake to generate WIX installer in newly created build directory
    """
    if sys.platform == 'win32':
        output_dir = args.output_dir
        cmake_spec = Spec('cmake')
        cmake_spec.concretize()
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
                spack_source = spack_source.replace('\\', '/')

        spack_version = args.spack_version

        here = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(here, "installer")
        posix_root = spack.paths.spack_root.replace('\\', '/')
        spack_license = posixpath.join(posix_root, "LICENSE-APACHE")
        rtf_spack_license = txt_to_rtf(spack_license)
        spack_license = posixpath.join(source_dir, "LICENSE.rtf")

        with open(spack_license, 'w') as rtf_license:
            written = rtf_license.write(rtf_spack_license)
            if written == 0:
                raise RuntimeError("Failed to generate properly formatted license file")
        spack_logo = posixpath.join(posix_root,
                                    "share/spack/logo/favicon.ico")

        try:
            subprocess.check_call(
                ('"%s" -S "%s" -B "%s" -DSPACK_VERSION=%s '
                 '-DSPACK_SOURCE="%s" -DSPACK_LICENSE="%s" '
                 '-DSPACK_LOGO="%s" -DSPACK_GIT_VERBOSITY="%s"')
                % (cmake_path, source_dir, output_dir, spack_version, spack_source,
                   spack_license, spack_logo, git_verbosity),
                shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer")
            return subprocess.CalledProcessError.returncode

        try:
            subprocess.check_call(
                '"%s" --config "%s/CPackConfig.cmake" -B "%s/"'
                % (cpack_path, output_dir, output_dir),
                shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer")
            return subprocess.CalledProcessError.returncode
        try:
            subprocess.check_call(
                '"%s/bin/candle.exe" -ext WixBalExtension "%s/bundle.wxs"'
                ' -out "%s/bundle.wixobj"'
                % (os.environ.get('WIX'), output_dir, output_dir), shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer chain")
            return subprocess.CalledProcessError.returncode
        try:
            subprocess.check_call(
                '"%s/bin/light.exe" -sw1134 -ext WixBalExtension "%s/bundle.wixobj"'
                ' -out "%s/Spack.exe"'
                % (os.environ.get('WIX'), output_dir, output_dir), shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer chain")
            return subprocess.CalledProcessError.returncode
        print("Successfully generated Spack.exe in %s" % (output_dir))
    else:
        print('The make-installer command is currently only supported on Windows.')
