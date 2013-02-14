import string

import spack
import spack.packages as packages
import spack.tty as tty
import spack.version

pacakge_tempate = string.Template("""\
from spack import *

class $name(Package):
    homepage = "${homepage}"
    url      = "${url}"
    md5      = "${md5}"

    def install(self):
        # Insert your installation code here.
        pass
""")

def create_template(name):
    class_name = name.capitalize()
    return new_pacakge_tempate % class_name


def setup_parser(subparser):
    subparser.add_argument('url', nargs='?', help="url of package archive")


def create(args):
    url = args.url

    version = spack.version.parse(url)
    if not version:
        tty.die("Couldn't figure out a version string from '%s'." % url)



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
