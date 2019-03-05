# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.prefix import Prefix
import os


class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: The PGI compilers are licensed software. You will need to create an
    account on the PGI homepage and download PGI yourself. Spack will search
    your current directory for the download tarball. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.pgroup.com/"

    version('19.1', sha256='3e05a6db2bf80b5d15f6ff83188f20cb89dc23e233417921e5c0822e7e57d34f')
    version('18.10', sha256='4b3ff83d2a13de6001bed599246eff8e63ef711b8952d4a9ee12efd666b3e326')
    version('18.4',  'b55461f9f0986acbd51902c51c2074b9')
    version('17.10', '85ad6506e7ada610ab11ddb35d697efa')
    version('17.4',  'a311d2756ddda657860bad8e5725597b')
    version('17.3',  '6eefc42f85e756cbaba76467ed640902')
    version('16.10', '9bb6bfb7b1052f9e6a45829ba7a24e47')
    version('16.5',  'a40e8852071b5d600cb42f31631b3de1')
    version('16.3',  '618cb7ddbc57d4e4ed1f21a0ab25f427')
    version('15.7',  '84a689217b17cdaf78c39270c70bea5d')

    variant('network', default=True,
            description="Perform a network install")
    variant('single',  default=False,
            description="Perform a single system install")
    variant('nvidia',  default=False,
            description="Enable installation of optional NVIDIA components")
    variant('amd',     default=False,
            description="Enable installation of optional AMD components")
    variant('java',    default=False,
            description="Enable installation of Java Runtime Environment")
    variant('mpi',     default=False,
            description="Enable installation of Open MPI")

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license.dat']
    license_vars = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url = 'http://www.pgroup.com/doc/pgiinstall.pdf'

    def url_for_version(self, version):
        if int(str(version.up_to(1))) <= 17:
            return "file://{0}/pgilinux-20{1}-{2}-x86_64.tar.gz".format(
                os.getcwd(), version.up_to(1), version.joined)
        else:
            return "file://{0}/pgilinux-20{1}-{2}-x86-64.tar.gz".format(
                os.getcwd(), version.up_to(1), version.joined)

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['PGI_SILENT'] = "true"
        os.environ['PGI_ACCEPT_EULA'] = "accept"
        os.environ['PGI_INSTALL_DIR'] = prefix

        if '+network' in spec and '~single' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "network"
            os.environ['PGI_INSTALL_LOCAL_DIR'] = "%s/%s/share_objects" % \
                (prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single '
            msg += 'system install.\nYou cannot choose both.'
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

    def setup_environment(self, spack_env, run_env):
        prefix = Prefix(join_path(self.prefix, 'linux86-64', self.version))

        run_env.set('CC',  join_path(prefix.bin, 'pgcc'))
        run_env.set('CXX', join_path(prefix.bin, 'pgc++'))
        run_env.set('F77', join_path(prefix.bin, 'pgfortran'))
        run_env.set('FC',  join_path(prefix.bin, 'pgfortran'))

        run_env.prepend_path('PATH',            prefix.bin)
        run_env.prepend_path('CPATH',           prefix.include)
        run_env.prepend_path('LIBRARY_PATH',    prefix.lib)
        run_env.prepend_path('LD_LIBRARY_PATH', prefix.lib)
        run_env.prepend_path('MANPATH',         prefix.man)
