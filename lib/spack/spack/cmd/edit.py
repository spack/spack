import os
import spack
import spack.packages as packages
import spack.tty as tty

description = "Open package files in $EDITOR"

def setup_parser(subparser):
    subparser.add_argument(
        'name', nargs='?', default=None, help="name of package to edit")


def edit(parser, args):
    name = args.name

    # By default open the directory where packages live.
    if not name:
        path = spack.packages_path
    else:
        path = packages.filename_for(name)

        if os.path.exists(path):
            if not os.path.isfile(path):
                tty.die("Something's wrong.  '%s' is not a file!" % path)
            if not os.access(path, os.R_OK|os.W_OK):
                tty.die("Insufficient permissions on '%s'!" % path)
        else:
            tty.die("No package for %s.  Use spack create.")

    # If everything checks out, go ahead and edit.
    spack.editor(path)
