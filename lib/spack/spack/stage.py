import os
import re
import shutil

import spack
import packages
import tty


def ensure_access(dir=spack.stage_path):
    if not os.access(dir, os.R_OK|os.W_OK):
        tty.die("Insufficient permissions on directory %s" % dir)


class Stage(object):
    def __init__(self, stage_name, url):
        self.stage_name = stage_name
        self.url = url

    @property
    def path(self):
        return spack.new_path(spack.stage_path, self.stage_name)


    def setup(self):
        if os.path.exists(self.path):
            if not os.path.isdir(self.path):
                tty.die("Stage path %s is not a directory!" % self.path)
        else:
            os.makedirs(self.path)

        ensure_access(self.path)


    @property
    def archive_file(self):
        path = os.path.join(self.path, os.path.basename(self.url))
        if os.path.exists(path):
            return path
        return None


    @property
    def expanded_archive_path(self):
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
        self.setup()
        if os.path.isdir(self.path):
            os.chdir(self.path)
        else:
            tty.die("Setup failed: no such directory: " + self.path)


    def fetch(self):
        """Downloads the file at URL to the stage.  Returns true if it was downloaded,
           false if it already existed."""
        self.chdir()
        if self.archive_file:
            tty.msg("Already downloaded %s." % self.archive_file)

        else:
            tty.msg("Fetching %s" % self.url)

            # Run curl but grab the mime type from the http headers
            headers = spack.curl('-#', '-O', '-D', '-', self.url, return_output=True)

            # output this if we somehow got an HTML file rather than the archive we
            # asked for.
            if re.search(r'Content-Type: text/html', headers):
                tty.warn("The contents of %s look like HTML.  The checksum will "+
                         "likely fail.  Use 'spack clean %s' to delete this file. "
                         "The fix the gateway issue and install again." % (self.archive_file, self.name))

        if not self.archive_file:
            raise FailedDownloadException(url)

        return self.archive_file


    def expand_archive(self):
        self.chdir()

        if not self.archive_file:
            tty.die("Attempt to expand archive before fetching.")

        decompress = spack.decompressor_for(self.archive_file)
        decompress(self.archive_file)


    def chdir_to_archive(self):
        """Changes directory to the expanded archive directory if it exists.
           Dies with an error otherwise.
        """
        path = self.expanded_archive_path
        if not path:
            tty.die("Attempt to chdir before expanding archive.")
        else:
            os.chdir(path)
            if not os.listdir(path):
                tty.die("Archive was empty for %s" % self.name)


    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands the archive."""
        if not self.archive_file:
            tty.die("Attempt to restage when not staged.")

        if self.expanded_archive_path:
            shutil.rmtree(self.expanded_archive_path, True)
        self.expand_archive()


    def destroy(self):
        """Blows away the stage directory.  Can always call setup() again."""
        if os.path.exists(self.path):
            shutil.rmtree(self.path, True)
