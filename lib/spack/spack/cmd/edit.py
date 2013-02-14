import os
import spack
import spack.packages as packages
import spack.tty as tty

new_pacakge_tempate = """\
from spack import *

class %s(Package):
    homepage = "https://www.example.com"
    url      = "https://www.example.com/download/example-1.0.tar.gz"
    md5      = "nomd5"

    def install(self):
        # Insert your installation code here.
        pass

"""

def create_template(name):
    class_name = name.capitalize()
    return new_pacakge_tempate % class_name


def setup_parser(subparser):
    subparser.add_argument(
        'name', nargs='?', default=None, help="name of package to edit")

def edit(args):
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
            tty.msg("Editing new file: '%s'." % path)
            file = open(path, "w")
            file.write(create_template(name))
            file.close()

    # If everything checks out, go ahead and edit.
    spack.editor(path)
