
description = "Run pydoc from within spack."

def setup_parser(subparser):
    subparser.add_argument('entity', help="Run pydoc help on entity")


def doc(parser, args):
    help(args.entity)
