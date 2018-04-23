from spack import *
from llnl.util import filesystem
import shutil
import os

# http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
def xcopytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def xinstall_tree(src, dest, **kwargs):
    """Manually install a file to a particular location."""
    #tty.debug("Installing %s to %s" % (src, dest))
    xcopytree(src, dest, **kwargs)

    for s, d in filesystem.traverse_tree(src, dest, follow_nonexisting=False):
        filesystem.set_install_permissions(d)
        filesystem.copy_mode(s, d)



class ArchdefsSrc(Package):
    """Build system (sort of) for GALAHAD and other optimization packages."""

    homepage = "http://ccpforge.cse.rl.ac.uk/gf/project/cutest/wiki"

    # Galahad has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('1.00000', svn='http://ccpforge.cse.rl.ac.uk/svn/cutest/archdefs/trunk/', revision=286)

    mainatiners = ['citibeth']

    def install(self, spec, prefix):
        # Google Test doesn't have a make install
        # We have to do our own install here.
	xinstall_tree('.', prefix)
