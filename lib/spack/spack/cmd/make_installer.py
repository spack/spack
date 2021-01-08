# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
import subprocess
import spack.paths

description = "generate Windows installer"
section = "admin"
level = "long"


def setup_parser(subparser):
    spack_source_group = subparser.add_mutually_exclusive_group(required=True)
    spack_source_group.add_argument(
        '-v', '--spack_version', default="",
        help='download given spack version e.g. 0.16.0')
    spack_source_group.add_argument(
        '-s', '--spack_source', default="",
        help='full path to spack source')

    subparser.add_argument(
        'output_dir', help="output directory")


def make_installer(parser, args):
    """
       Use CMake to generate WIX installer in newly created build directory
    """
    if(sys.platform == 'win32'):
        output_dir = args.output_dir

        spack_source = args.spack_source
        if spack_source:
            if not os.path.exists(spack_source):
                print("%s does not exist" % spack_source)
                return
            else:
                spack_source = os.path.abspath(spack_source)
                spack_source = spack_source.replace("\\", "/")

        spack_version = args.spack_version

        here = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(here, "installer")

        spack_license = os.path.join(spack.paths.spack_root, "LICENSE-APACHE")
        spack_license = spack_license.replace("\\", "/")

        spack_logo = os.path.join(spack.paths.spack_root,
                                  "share/spack/logo/favicon.ico")
        spack_logo = spack_logo.replace("\\", "/")

        try:
            subprocess.check_call(
                ('cmake -S "%s" -B "%s" -DSPACK_VERSION=%s '
                 '-DSPACK_SOURCE="%s" -DSPACK_LICENSE="%s" -DSPACK_LOGO="%s"')
                % (source_dir, output_dir, spack_version, spack_source,
                   spack_license, spack_logo),
                shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer")
            return

        try:
            subprocess.check_call(
                'cpack --config "%s/CPackConfig.cmake" -B "%s/"'
                % (output_dir, output_dir),
                shell=True)
        except subprocess.CalledProcessError:
            print("Failed to generate installer")
            return
    else:
        print('The generate command is currently only supported on Windows.')
