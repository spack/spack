from spack import *
import spack
import llnl.util.tty as tty
import os

class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: The PGI compilers are licensed software. You will need to create
    an account on the PGI homepage and download PGI yourself. Once the download
    finishes, rename the file (which may contain information such as the
    architecture) to the format: pgi-<version>.tar.gz. Spack will search your
    current directory for a file of this format. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "http://www.pgroup.com/"
    url      = "file://%s/pgi-16.3.tar.gz" % os.getcwd()

    version('16.3', '618cb7ddbc57d4e4ed1f21a0ab25f427')

    variant('network', default=True,  description="Perform a network install")
    variant('single',  default=False, description="Perform a single system install")
    variant('nvidia',  default=False, description="Enable installation of optional NVIDIA components, such as CUDA")
    variant('amd',     default=False, description="Enable installation of optional AMD components")
    variant('java',    default=False, description="Enable installation of Java Runtime Environment")
    variant('mpi',     default=False, description="Enable installation of Open MPI")


    def set_up_license(self, prefix):
        license_path = "%s/license.dat" % prefix

        with open(license_path, "w") as license:
            license.write("""\
# The PGI compilers require a license to use. There are two ways to set this up.
#
# 1.    (Recommended) Store your license key in this license.dat file. Example:
#
#       SERVER <hostname> 0123456789ab 27000
#       DAEMON pgroupd
#       PACKAGE PGI2015-<PGI_PIN> pgroupd <subscription end date>  A13AB920D570 \\
#       <...>
#       6167 7015 3F05 9C37 2315 ACDF 1B73 DAA9 FBAE"
#
# 2.    Use the environment variable PGROUPD_LICENSE_FILE or LM_LICENSE_FILE.
#
#       If you choose to store your license in a non-standard location, you may
#       set either one of these variables to a full pathname to the license
#       file, or port@host if you store your license keys on a dedicated
#       license server. You will likely want to set this variable in a module
#       file so that it gets loaded every time someone wants to use PGI.
#
# For further information on how to acquire a license, please refer to:
# http://www.pgroup.com/doc/pgiinstall.pdf
#
# You may enter your license below.

""")

        #spack.editor(license_path)
        tty.msg("Set up license file %s" % license_path)


    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['PGI_SILENT'] = "true"
        os.environ['PGI_ACCEPT_EULA'] = "accept"
        os.environ['PGI_INSTALL_DIR'] = "%s" % prefix

        if '+network' in spec and '~single' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "network"
            os.environ['PGI_INSTALL_LOCAL_DIR'] = "%s/%s/share_objects" % (prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single system install.\n'
            msg += 'You cannot choose both.'
            raise RuntimeError(msg)

        if '+nvidia' in spec:
            os.environ['PGI_INSTALL_NVIDIA'] = "true"

        if '+amd' in spec:
            os.environ['PGI_INSTALL_AMD'] = "true"

        if '+java' in spec:
            os.environ['PGI_INSTALL_JAVA'] = "true"

        if '+mpi' in spec:
            os.environ['PGI_INSTALL_MPI'] = "true"

        # Run install script
        os.system("./install")

        # Prompt user to set up license file
        self.set_up_license(prefix)
