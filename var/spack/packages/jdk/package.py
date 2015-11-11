#------------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
#------------------------------------------------------------------------------
import distutils
from distutils import dir_util
from subprocess import call

import spack
from spack import *
import llnl.util.tty as tty

class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation
       in the form of a binary product aimed at Java developers."""
    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    version('8u25-linux-x64', 'e145c03a7edc845215092786bcfba77e',
        url="http://download.oracle.com/otn-pub/java/jdk/8u25-b17/jdk-8u25-linux-x64.tar.gz")

    # Oracle requires that you accept their License Agreement in order
    # to access the Java packages in download.oracle.com. In order to
    # automate this process, we need to utilize these additional curl
    # commandline options.
    #
    # See http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux
    curl_options=[
        '-j', # junk cookies
        '-H', # specify required License Agreement cookie
        'Cookie: oraclelicense=accept-securebackup-cookie']

    def do_fetch(self):
        # Add our custom curl commandline options
        tty.msg(
            "[Jdk] Adding required commandline options to curl " +
            "before performing fetch: %s" %
            (self.curl_options))

        for option in self.curl_options:
            spack.curl.add_default_arg(option)

        # Now perform the actual fetch
        super(Jdk, self).do_fetch()


    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)
