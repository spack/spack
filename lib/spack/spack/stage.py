import os
import re
import shutil
import tempfile
import getpass

import spack
import packages
import tty


def ensure_access(dir=spack.stage_path):
    if not os.access(dir, os.R_OK|os.W_OK):
        tty.die("Insufficient permissions on directory %s" % dir)


def purge():
    """Remove the entire stage path."""
    if os.path.isdir(spack.stage_path):
        shutil.rmtree(spack.stage_path, True)


class Stage(object):
    def __init__(self, stage_name, url):
        self.stage_name = stage_name
        self.url = url

    @property
    def path(self):
        return spack.new_path(spack.stage_path, self.stage_name)


    def setup(self):
        # If the user switched stage types on us, destroy the old one and
        # start over
        if spack.use_tmp_stage:
            if not os.path.islink(self.path):
                self.destroy()
        else:
            if os.path.islink(self.path):
                self.destroy()

        if os.path.exists(self.path):
            if not os.path.isdir(self.path):
                tty.die("Stage path %s is not a directory!" % self.path)
        else:
            # Now create the stage directory
            spack.mkdirp(spack.stage_path)

            # And the stage for this build within it
            if not spack.use_tmp_stage:
                # non-tmp stage is just a directory in spack.stage_path
                spack.mkdirp(self.path)
            else:
                # tmp stage is created in tmp but linked to spack.stage_path
                tmp_dir = next((tmp for tmp in spack.tmp_dirs
                               if os.access(tmp, os.R_OK|os.W_OK)), None)

                username = getpass.getuser()
                if username:
                    tmp_dir = spack.new_path(tmp_dir, username)
                spack.mkdirp(tmp_dir)
                tmp_dir = tempfile.mkdtemp(
                    '.stage', self.stage_name + '-', tmp_dir)

                os.symlink(tmp_dir, self.path)

        ensure_access(self.path)


    @property
    def archive_file(self):
        path = os.path.join(self.path, os.path.basename(self.url))
        if os.path.exists(path):
            return path
        return None


    @property
    def expanded_archive_path(self):
        """Returns the path to the expanded archive directory if it's expanded;
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
            headers = spack.curl('-#',        # status bar
                                 '-O',        # save file to disk
                                 '-D', '-',   # print out HTML headers
                                 '-L', self.url, return_output=True)

            # Check if we somehow got an HTML file rather than the archive we
            # asked for.  We only look at the last content type, to handle
            # redirects properly.
            content_types = re.findall(r'Content-Type:[^\r\n]+', headers)
            if content_types and 'text/html' in content_types[-1]:
                tty.warn("The contents of " + self.archive_file + " look like HTML.",
                         "The checksum will likely be bad.  If it is, you can use",
                         "'spack clean --all' to remove the bad archive, then fix",
                         "your internet gateway issue and install again.")

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
            if os.path.islink(self.path):
                shutil.rmtree(os.path.realpath(self.path), True)
                os.unlink(self.path)
            else:
                shutil.rmtree(self.path, True)
