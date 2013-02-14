import spack
from spack.fileutils import *

import re
import inspect


def filename_for(package):
    """Get the filename where a package name should be stored."""
    return new_path(spack.packages_path, "%s.py" % package.lower())


def get(name):
    file = filename_for(name)

    if os.path.exists(file):
        if not os.path.isfile(file):
            tty.die("Something's wrong. '%s' is not a file!" % file)
        if not os.access(file, os.R_OK):
            tty.die("Cannot read '%s'!" % file)

    class_name = name.capitalize()
    try:
        module_name = "%s.%s" % (__name__, name)
        module = __import__(module_name, fromlist=[class_name])
    except ImportError, e:
        tty.die("Error while importing %s.%s:\n%s" % (name, class_name, e.message))

    klass = getattr(module, class_name)
    if not inspect.isclass(klass):
        tty.die("%s.%s is not a class" % (name, class_name))

    return klass


