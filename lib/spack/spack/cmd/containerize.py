# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import tempfile
from typing import Optional

import llnl.util.tty

import spack.cmd
import spack.container
import spack.container.images
import spack.oci.oci
import spack.stage
from spack.cmd.buildcache import (
    _archspec_to_gooarch,
    _make_pool,
    _push_oci,
    _put_manifest,
    copy_missing_layers_with_retry,
    default_config,
    default_manifest,
)
from spack.cmd.common import arguments
from spack.oci.image import ImageReference

description = "creates recipes to build images for different container runtimes"
section = "container"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="subcommand")
    recipe_parser = sp.add_parser("recipe", help="Create a recipe to build a container image")
    recipe_parser.add_argument(
        "--list-os",
        action="store_true",
        default=False,
        help="list all the OS that can be used in the bootstrap phase and exit",
    )
    recipe_parser.add_argument(
        "--last-stage",
        choices=("bootstrap", "build", "final"),
        default="final",
        help="last stage in the container recipe",
    )

    oci_parser = sp.add_parser(
        "oci", help="Create a container image out of a locally installed Spack environment"
    )
    oci_parser.add_argument("--base-image")
    oci_parser.add_argument("--force", default=False, action="store_true")
    oci_parser.add_argument("--tag", "-t", required=True)
    oci_parser.add_argument("mirror", type=arguments.mirror_name_or_url)


def containerize(parser, args):
    if args.subcommand == "oci":
        containerize_oci(parser, args)
    elif args.subcommand == "recipe":
        containerize_recipe(parser, args)


def containerize_oci(parser, args):
    image_ref = spack.oci.oci.image_from_mirror(args.mirror)
    env = spack.cmd.require_active_env("containerize oci")
    roots = env.concrete_roots()

    base_image_ref: Optional[ImageReference] = (
        ImageReference.from_string(args.base_image) if args.base_image else None
    )

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
        with _make_pool() as pool:
            _, base_images, checksums = _push_oci(args, image_ref, env.all_specs(), tmpdir, pool)

        architecture = _archspec_to_gooarch(roots[0])

        if architecture not in base_images:
            if base_image_ref is None:
                base_images[architecture] = (
                    default_manifest(),
                    default_config(architecture, "linux"),
                )
            else:
                base_images[architecture] = copy_missing_layers_with_retry(
                    base_image_ref, image_ref, architecture
                )

        # Add a manifest for the environment
        environment_tag = image_ref.with_tag(args.tag)
        _put_manifest(
            base_images, checksums, environment_tag, tmpdir, None, None, *env.concrete_roots()
        )

        llnl.util.tty.info(f"Pushed {environment_tag}")


def containerize_recipe(parser, args):
    if args.list_os:
        possible_os = spack.container.images.all_bootstrap_os()
        msg = "The following operating systems can be used to bootstrap Spack:"
        msg += "\n{0}".format(" ".join(possible_os))
        llnl.util.tty.msg(msg)
        return

    config_dir = args.env_dir or os.getcwd()
    config_file = os.path.abspath(os.path.join(config_dir, "spack.yaml"))
    if not os.path.exists(config_file):
        msg = "file not found: {0}"
        raise ValueError(msg.format(config_file))

    config = spack.container.validate(config_file)
    recipe = spack.container.recipe(config, last_phase=args.last_stage)
    print(recipe)
