# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.sbom
import spack.util.spack_json as sjson
from spack.error import SpackError

description = "generate or view software bill of materials (sbom)"
section = "build"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='sbom_command')

    # Find (view) an existing path of an sbom
    path_parser = sp.add_parser('path', description="get the path to an existing sbom")

    # Create an sbom on the fly
    create_parser = sp.add_parser('create',
                                  description="create an sbom if it does not exist.")

    # Show the file contents in the terminal
    show_parser = sp.add_parser('show',
                                description="dump an existing sbom to the terminal.")

    # Every parser accepts a spec
    for parser in [create_parser, path_parser, show_parser]:
        parser.add_argument("spec", help="spec name for sbom")


def sbom(parser, args, **kwargs):
    try:
        specs = spack.cmd.parse_specs([args.spec], concretize=True)
    except SpackError as e:
        tty.die(e)

    # Just generate for one spec
    spec = specs[0]

    # Do not proceed if spec isn't installed!
    if not spec.install_status():
        tty.die("That spec is not installed. Try spack install with --sbom.")

    # sbom required to exist for show and path
    if args.sbom_command in ["show", "path"]:
        sbom_file = spack.sbom.find_sbom(spec)
        if not sbom_file:
            tty.die("sbom for that spec does not exist. Use spack sbom create.")

        if args.sbom_command == "path":
            tty.info(sbom_file)
        elif args.sbom_command == "show":
            with open(sbom_file, 'r') as f:
                print(sjson.dump(sjson.load(f.read())))

    # Show the path of an existing sbom
    elif args.sbom_command == "path":
        path = spack.sbom.find_sbom(spec)
        if not path:
            tty.die("sbom for that spec does not exist. Use spack sbom create.")
        tty.info(path)

    elif args.sbom_command == "create":
        sbom_file = spack.sbom.create_sbom(spec)
        tty.info("sbom generated successfully: %s" % sbom_file)
