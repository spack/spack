import os
import re
import shutil
import tempfile
import getpass

import spack
import spack.error as serr
import tty

class FailedDownloadError(serr.SpackError):
    """Raised wen a download fails."""
    def __init__(self, url):
        super(FailedDownloadError, self).__init__(
            "Failed to fetch file from URL: " + url)
        self.url = url


class Stage(object):
    """A Stage object manaages a directory where an archive is downloaded,
       expanded, and built before being installed.  A stage's lifecycle looks
       like this:

       setup()           Create the stage directory.
       fetch()           Fetch a source archive into the stage.
       expand_archive()  Expand the source archive.
       <install>         Build and install the archive.  This is handled
                         by the Package class.
       destroy()         Remove the stage once the package has been installed.

       If spack.use_tmp_stage is True, spack will attempt to create stages
       in a tmp directory.  Otherwise, stages are created directly in
       spack.stage_path.
    """

    def __init__(self, stage_name, url):
        """Create a stage object.
           Parameters:
             stage_name   Name of the stage directory that will be created.
             url          URL of the archive to be downloaded into this stage.
        """
        self.stage_name = stage_name
        self.url = url

    @property
    def path(self):
        """Absolute path to the stage directory."""
        return spack.new_path(spack.stage_path, self.stage_name)


    def setup(self):
        """Creates the stage directory.
           If spack.use_tmp_stage is False, the stage directory is created
           directly under spack.stage_path.

           If spack.use_tmp_stage is True, this will attempt to create a
           stage in a temporary directory and link it into spack.stage_path.
           Spack will use the first writable location in spack.tmp_dirs to
           create a stage.  If there is no valid location in tmp_dirs, fall
           back to making the stage inside spack.stage_path.
        """
        # If we're using a stage in tmp that has since been deleted,
        # remove the stale symbolic link.
        if os.path.islink(self.path):
            real_path = os.path.realpath(self.path)
            if not os.path.exists(real_path):
                os.unlink(self.path)

        # If the user switched stage modes, destroy the old stage and
        # start over.  We could move the old archive, but that seems
        # like a pain when we could just fetch it again.
        if spack.use_tmp_stage:
            if not os.path.islink(self.path):
                self.destroy()
        else:
            if os.path.islink(self.path):
                self.destroy()

        # Make sure that the stage is actually a directory.  Something
        # is seriously wrong if it's not.
        if os.path.exists(self.path):
            if not os.path.isdir(self.path):
                tty.die("Stage path %s is not a directory!" % self.path)
        else:
            # Create the top-level stage directory
            spack.mkdirp(spack.stage_path)

            # Find a tmp_dir if we're supposed to use one.
            tmp_dir = None
            if spack.use_tmp_stage:
                tmp_dir = next((tmp for tmp in spack.tmp_dirs
                                if can_access(tmp)), None)

            if not tmp_dir:
                # If we couldn't find a tmp dir or if we're not using tmp
                # stages, create the stage directly in spack.stage_path.
                spack.mkdirp(self.path)

            else:
                # Otherwise we found a tmp_dir, so create the stage there
                # and link it back to the prefix.
                username = getpass.getuser()
                if username:
                    tmp_dir = spack.new_path(tmp_dir, username)
                spack.mkdirp(tmp_dir)
                tmp_dir = tempfile.mkdtemp(
                    '.stage', self.stage_name + '-', tmp_dir)

                os.symlink(tmp_dir, self.path)

        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)


    @property
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        path = os.path.join(self.path, os.path.basename(self.url))
        if os.path.exists(path):
            return path
        return None


    @property
    def expanded_archive_path(self):
        """Returns the path to the expanded archive directory if it's expanded;
           None if the archive hasn't been expanded.
        """
        if not self.archive_file:
            return None

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

            try:
                # Run curl but grab the mime type from the http headers
                headers = spack.curl('-#',        # status bar
                                     '-O',        # save file to disk
                                     '-D', '-',   # print out HTML headers
                                     '-L', self.url, return_output=True)
            except:
                # clean up archive on failure.
                if self.archive_file:
                    os.remove(self.archive_file)
                raise

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
            raise FailedDownloadError(url)

        return self.archive_file


    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
           archive.  Fail if the stage is not set up or if the archive is not yet
           downloaded.
        """
        self.chdir()

        if not self.archive_file:
            tty.die("Attempt to expand archive before fetching.")

        decompress = spack.decompressor_for(self.archive_file)
        decompress(self.archive_file)


    def chdir_to_archive(self):
        """Changes directory to the expanded archive directory.
           Dies with an error if there was no expanded archive.
        """
        path = self.expanded_archive_path
        if not path:
            tty.die("Attempt to chdir before expanding archive.")
        else:
            os.chdir(path)
            if not os.listdir(path):
                tty.die("Archive was empty for %s" % self.name)


    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
           the archive.
        """
        if not self.archive_file:
            tty.die("Attempt to restage when not staged.")

        if self.expanded_archive_path:
            shutil.rmtree(self.expanded_archive_path, True)
        self.expand_archive()


    def destroy(self):
        """Remove this stage directory."""
        remove_linked_tree(self.path)



def can_access(file=spack.stage_path):
    """True if we have read/write access to the file."""
    return os.access(file, os.R_OK|os.W_OK)


def ensure_access(file=spack.stage_path):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def remove_linked_tree(path):
    """Removes a directory and its contents.  If the directory is a symlink,
       follows the link and reamoves the real directory before removing the
       link.
    """
    if os.path.exists(path):
        if os.path.islink(path):
            shutil.rmtree(os.path.realpath(path), True)
            os.unlink(path)
        else:
            shutil.rmtree(path, True)


def purge():
    """Remove all build directories in the top-level stage path."""
    if os.path.isdir(spack.stage_path):
        for stage_dir in os.listdir(spack.stage_path):
            stage_path = spack.new_path(spack.stage_path, stage_dir)
            remove_linked_tree(stage_path)
