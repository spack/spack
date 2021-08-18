# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.monitor

description = "interact with a monitor server"
section = "analysis"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='monitor_command')

    # This adds the monitor group to the subparser
    spack.monitor.get_monitor_group(subparser)

    # Spack Monitor Uploads
    monitor_parser = sp.add_parser('upload', description="upload to spack monitor")
    monitor_parser.add_argument("upload_dir", help="directory root to upload")


def monitor(parser, args, **kwargs):

    if args.monitor_command == "upload":
        monitor = spack.monitor.get_client(
            host=args.monitor_host,
            prefix=args.monitor_prefix,
            disable_auth=args.monitor_disable_auth,
        )

        # Upload the directory
        monitor.upload_local_save(args.upload_dir)
