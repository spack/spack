import spack.packages as packages
import spack.tty as tty
import spack.stage as stage

description = "Remove staged files for packages"

def setup_parser(subparser):
    subparser.add_argument('names', nargs='+', help="name(s) of package(s) to clean")
    subparser.add_argument('-c', "--clean", action="store_true", dest='clean',
                           help="run make clean in the stage directory (default)")
    subparser.add_argument('-w', "--work", action="store_true", dest='work',
                           help="delete and re-expand the entire stage directory")
    subparser.add_argument('-d', "--dist", action="store_true", dest='dist',
                           help="delete the downloaded archive.")


def clean(parser, args):
    if not args.names:
        tty.die("spack clean requires at least one package name.")

    for name in args.names:
        package = packages.get(name)
        if args.dist:
            package.do_clean_dist()
        elif args.work:
            package.do_clean_work()
        else:
            package.do_clean()
