import os
import shutil

import spack
import tty


def ensure_access(dir=spack.stage_path):
    if not os.access(dir, os.R_OK|os.W_OK):
        tty.die("Insufficient permissions on directory '%s'" % dir)


class Stage(object):
    def __init__(self, stage_name):
        self.stage_name = stage_name

    @property
    def path(self):
        return spack.new_path(spack.stage_path, self.stage_name)


    def setup(self):
        if os.path.exists(self.path):
            if not os.path.isdir(self.path):
                tty.die("Stage path '%s' is not a directory!" % self.path)
        else:
            os.makedirs(self.path)

        ensure_access(self.path)


    @property
    def archive_path(self):
        """"Returns the path to the expanded archive directory if it's expanded;
            None if the archive hasn't been expanded.
        """
        for file in os.listdir(self.path):
            archive_path = spack.new_path(self.path, file)
            if os.path.isdir(archive_path):
                return archive_path
        return None


    def chdir(self):
        """Changes directory to the stage path.  Or dies if it is not set up."""
        if os.path.isdir(self.path):
            os.chdir(self.path)
        else:
            tty.die("Attempt to chdir to stage before setup.")


    def chdir_to_archive(self):
        """Changes directory to the expanded archive directory if it exists.
           Dies with an error otherwise.
        """
        path = self.archive_path
        if not path:
            tty.die("Attempt to chdir before expanding archive.")
        else:
            os.chdir(path)
            if not os.listdir(path):
                tty.die("Archive was empty for '%s'" % self.name)


    def destroy(self):
        """Blows away the stage directory.  Can always call setup() again."""
        if os.path.exists(self.path):
            shutil.rmtree(self.path, True)
