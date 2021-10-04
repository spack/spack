# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path

import spack.container
import spack.monitor

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def setup_parser(subparser):
    monitor_group = spack.monitor.get_monitor_group(subparser)  # noqa


def containerize(parser, args):
    config_dir = args.env_dir or os.getcwd()
    config_file = os.path.abspath(os.path.join(config_dir, 'spack.yaml'))
    if not os.path.exists(config_file):
        msg = 'file not found: {0}'
        raise ValueError(msg.format(config_file))

    config = spack.container.validate(config_file)

    # If we have a monitor request, add monitor metadata to config
    if args.use_monitor:
        config['spack']['monitor'] = {"disable_auth": args.monitor_disable_auth,
                                      "host": args.monitor_host,
                                      "keep_going": args.monitor_keep_going,
                                      "prefix": args.monitor_prefix,
                                      "tags": args.monitor_tags}
    recipe = spack.container.recipe(config)
    print(recipe)
