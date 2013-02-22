import sys

description = "Get help on spack and its commands"

def setup_parser(subparser):
    subparser.add_argument('help_command', nargs='?', default=None,
                           help='command to get help on')

def help(parser, args):
    if args.help_command:
        parser.parse_args([args.help_command, '-h'])
    else:
        parser.print_help()
