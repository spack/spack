import os
import string
from contextlib import closing

import spack
import spack.packages as packages
import spack.tty as tty

description = "Open package files in $EDITOR"

# When -f is supplied, we'll create a very minimal skeleton.
package_template = string.Template("""\
from spack import *

class ${class_name}(Package):
    ""\"Description""\"

    homepage = "http://www.example.com"
    url      = "http://www.example.com/${name}-1.0.tar.gz"

    versions = { '1.0' : '0123456789abcdef0123456789abcdef' }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
""")


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', dest='force', action='store_true',
        help="Open a new file in $EDITOR even if package doesn't exist.")
    subparser.add_argument(
        'name', nargs='?', default=None, help="name of package to edit")


def edit(parser, args):
    name = args.name

    # By default open the directory where packages live.
    if not name:
        path = spack.packages_path
    else:
        path = packages.filename_for_package_name(name)

        if os.path.exists(path):
            if not os.path.isfile(path):
                tty.die("Something's wrong.  '%s' is not a file!" % path)
            if not os.access(path, os.R_OK|os.W_OK):
                tty.die("Insufficient permissions on '%s'!" % path)
        elif not args.force:
            tty.die("No package '%s'.  Use spack create, or supply -f/--force "
                    "to edit a new file." % name)
        else:
            class_name = packages.class_name_for_package_name(name)

            with closing(open(path, "w")) as pkg_file:
                pkg_file.write(
                    package_template.substitute(name=name, class_name=class_name))

    # If everything checks out, go ahead and edit.
    spack.editor(path)
