import string
import os

import spack
import spack.packages as packages
import spack.tty as tty
import spack.version

from spack.stage import Stage
from contextlib import closing

package_template = string.Template("""\
from spack import *

class ${class_name}(Package):
    homepage = "http://www.example.com"
    url      = "${url}"
    md5      = "${md5}"

    def install(self, prefix):
        # Insert the configure line for your build system here.
        configure("--prefix=%s" % prefix)
        # cmake(".", *std_cmake_args)
        make()
        make("install")
""")


def setup_parser(subparser):
    subparser.add_argument('url', nargs='?', help="url of package archive")
    subparser.add_argument('-f', '--force', action='store_true', dest='force',
                           help="Remove existing package file.")


def create(parser, args):
    url = args.url

    # Try to deduce name and version of the new package from the URL
    name, version = spack.version.parse(url)
    if not name:
        print "Couldn't guess a name for this package."
        while not name:
            new_name = raw_input("Name: ")
            if packages.valid_name(name):
                name = new_name
            else:
                print "Package names must contain letters, numbers, and '_' or '-'"

    if not version:
        tty.die("Couldn't guess a version string from %s." % url)

    path = packages.filename_for(name)
    if not args.force and os.path.exists(path):
        tty.die("%s already exists." % path)

    # make a stage and fetch the archive.
    try:
        stage = Stage("%s-%s" % (name, version), url)
        archive_file = stage.fetch()
    except spack.FailedDownloadException, e:
        tty.die(e.message)

    md5 = spack.md5(archive_file)
    class_name = packages.class_for(name)

    # Write outa template for the file
    tty.msg("Editing %s." % path)
    with closing(open(path, "w")) as pkg_file:
        pkg_file.write(
            package_template.substitute(
                class_name=class_name,
                url=url,
                md5=md5))

    # If everything checks out, go ahead and edit.
    spack.editor(path)
