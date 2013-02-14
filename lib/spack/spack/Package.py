import inspect
import os
import re
import subprocess

from spack import *
import tty
import attr
import validate
import version
import shutil
import platform
from stage import Stage

def depends_on(*args, **kwargs):
    """Adds a depends_on local variable in the locals of
       the calling class, based on args.
    """
    stack = inspect.stack()
    try:
        locals = stack[1][0].f_locals
    finally:
        del stack
    print locals

    locals["depends_on"] = kwargs


class Package(object):
    def __init__(self):
        attr.required(self, 'homepage')
        attr.required(self, 'url')
        attr.required(self, 'md5')

        # Name of package is just the classname lowercased
        self.name = self.__class__.__name__.lower()

        # Make sure URL is an allowed type
        validate.url(self.url)

        v = version.parse(self.url)
        if not v:
            tty.die("Couldn't extract version from '%s'. " +
                    "You must specify it explicitly for this URL." % self.url)
        self.version = v

    @property
    def stage(self):
        return Stage(self.stage_name)

    @property
    def stage_name(self):
        return "%s-%s" % (self.name, self.version)

    @property
    def prefix(self):
        return new_path(install_path, self.stage_name)

    def do_fetch(self):
        """Creates a stage directory and downloads the taball for this package.
           Working directory will be set to the stage directory.
        """
        stage = self.stage
        stage.setup()
        stage.chdir()

        archive_file = os.path.basename(self.url)
        if not os.path.exists(archive_file):
            tty.msg("Fetching %s" % self.url)

            # Run curl but grab the mime type from the http headers
            headers = curl('-#', '-O', '-D', '-', self.url, return_output=True)

            # output this if we somehow got an HTML file rather than the archive we
            # asked for.
            if re.search(r'Content-Type: text/html', headers):
                tty.warn("The contents of '%s' look like HTML.  The checksum will "+
                         "likely fail.  Use 'spack clean %s' to delete this file. "
                         "The fix the gateway issue and install again." % (archive_file, self.name))

            if not os.path.exists(archive_file):
                tty.die("Failed to download '%s'!" % self.url)
        else:
            tty.msg("Already downloaded %s." % self.name)

        archive_md5 = md5(archive_file)
        if archive_md5 != self.md5:
            tty.die("MD5 Checksum failed for %s.  Expected %s but got %s."
                    % (self.name, self.md5, archive_md5))

        return archive_file

    def do_stage(self):
        """Unpacks the fetched tarball, then changes into the expanded tarball directory."""
        archive_file = self.do_fetch()
        stage = self.stage

        archive_dir = stage.archive_path
        if not archive_dir:
            tty.msg("Staging archive: '%s'" % archive_file)
            decompress = decompressor_for(archive_file)
            decompress(archive_file)
        else:
            tty.msg("Alredy staged %s" % self.name)

        stage.chdir_to_archive()

    def do_install(self):
        """This class should call this version of the install method.
           Package implementations should override install().
        """
        if os.path.exists(self.prefix):
            tty.msg("%s is already installed." % self.name)
            tty.pkg(self.prefix)
            return

        self.do_stage()

        # Populate the module scope of install() with some useful functions.
        # This makes things easier for package writers.
        self.module.configure = which("configure", [self.stage.archive_path])
        self.module.cmake = which("cmake")

        self.install(self.prefix)
        tty.msg("Successfully installed %s" % self.name)
        tty.pkg(self.prefix)

    @property
    def module(self):
        """Use this to add variables to the class's module's scope.
           This lets us use custom syntax in the install method.
        """
        return __import__(self.__class__.__module__,
                          fromlist=[self.__class__.__name__])

    def install(self, prefix):
        """Package implementations override this with their own build configuration."""
        tty.die("Packages must provide an install method!")

    def do_uninstall(self):
        self.uninstall(self.prefix)
        tty.msg("Successfully uninstalled %s." % self.name)

    def uninstall(self, prefix):
        """By default just blows the install dir away."""
        shutil.rmtree(self.prefix, True)

    def do_clean(self):
        self.clean()

    def clean(self):
        """By default just runs make clean.  Override if this isn't good."""
        stage = self.stage
        if stage.archive_path:
            stage.chdir_to_archive()
            try:
                make("clean")
                tty.msg("Successfully cleaned %s" % self.name)
            except subprocess.CalledProcessError:
                # Might not be configured.  Ignore.
                pass

    def do_clean_all(self):
        if os.path.exists(self.stage.path):
            self.stage.destroy()
        tty.msg("Successfully cleaned %s" % self.name)


