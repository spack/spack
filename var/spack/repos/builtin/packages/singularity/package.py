# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import llnl.util.tty as tty
import os
import shutil


class Singularity(MakefilePackage):
    '''Singularity is a container technology focused on building portable
       encapsulated environments to support "Mobility of Compute" For older
       versions of Singularity (pre 3.0) you should use singularity-legacy,
       which has a different install base (Autotools).

       Needs post-install chmod/chown steps to enable full functionality.
       See package definition for details.
    '''

    homepage = "https://www.sylabs.io/singularity/"
    url      = "https://github.com/sylabs/singularity/releases/download/v3.1.1/singularity-3.1.1.tar.gz"
    git      = "https://github.com/sylabs/singularity.git"

    version('develop', branch='master')
    version('3.1.1', '158f58a79db5337e1d655ee0159b641e42ea7435')

    depends_on('go')
    depends_on('libuuid')
    depends_on('libgpg-error')
    depends_on('squashfs', type='run')
    depends_on('git', when='@develop')  # mconfig uses it for version info

    # Go has novel ideas about how projects should be organized.
    # We'll point GOPATH at the stage dir, and move the unpacked src
    # tree into the proper subdir in our overridden do_stage below.
    @property
    def gopath(self):
        return join_path(self.stage.path)

    @property
    def sylabs_gopath_dir(self):
        return join_path(self.gopath, 'src/github.com/sylabs/')

    @property
    def singularity_gopath_dir(self):
        return join_path(self.sylabs_gopath_dir, 'singularity')

    # Unpack the tarball as usual, then move the src dir into
    # its home within GOPATH.
    def do_stage(self, mirror_only=False):
        super(Singularity, self).do_stage(mirror_only)
        source_path = self.stage.source_path
        if not os.path.exists(self.singularity_gopath_dir):
            tty.debug("Moving {0} to {1}".format(
                source_path, self.singularity_gopath_dir))
            mkdirp(self.sylabs_gopath_dir)
            shutil.move(source_path,
                        self.singularity_gopath_dir)

    # MakefilePackage's stages use this via working_dir()
    @property
    def build_directory(self):
        return self.singularity_gopath_dir

    # Hijack the edit stage to run mconfig.
    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            configure = Executable('./mconfig --prefix=%s' % prefix)
            configure()

    # Set these for use by MakefilePackage's default build/install methods.
    build_targets = ['-C', 'builddir', 'parallel=False']
    install_targets = ['install', '-C', 'builddir', 'parallel=False']

    def setup_environment(self, spack_env, run_env):
        # Point GOPATH at the top of the staging dir for the build
        # step.
        spack_env.prepend_path('GOPATH', self.gopath)

    # `singularity` has a fixed path where it will look for
    # mksquashfs.  If it lives somewhere else you need to specify the
    # full path in the config file.  This bit uses filter_file to edit
    # the config file, uncommenting and setting the mksquashfs path.
    @run_after('install')
    def fix_mksquashfs_path(self):
        prefix = self.spec.prefix
        squash_path = join_path(self.spec['squashfs'].prefix.bin, 'mksquashfs')
        filter_file(r'^# mksquashfs path =',
                    'mksquashfs path = {0}'.format(squash_path),
                    join_path(prefix.etc, 'singularity', 'singularity.conf'))

    #
    # Assemble a script that fixes the ownership and permissions of several
    # key files, install it, and tty.warn() the user.
    # HEADSUP: https://github.com/spack/spack/pull/10412.
    #
    def perm_script(self):
        return 'spack_perms_fix.sh'

    def perm_script_tmpl(self):
        return "{0}.j2".format(self.perm_script())

    def perm_script_path(self):
        return join_path(self.spec.prefix.bin, self.perm_script())

    def _build_script(self, filename, variable_data):
        with open(filename, 'w') as f:
            env = spack.tengine.make_environment(dirs=self.package_dir)
            t = env.get_template(self.perm_script_tmpl())
            f.write(t.render(variable_data))

    @run_after('install')
    def build_perms_script(self):
        script = self.perm_script_path()
        chown_files = ['libexec/singularity/bin/starter-suid',
                       'etc/singularity/singularity.conf',
                       'etc/singularity/capability.json',
                       'etc/singularity/ecl.toml']
        setuid_files = ['libexec/singularity/bin/starter-suid']
        self._build_script(script, {'prefix': self.spec.prefix,
                                    'chown_files': chown_files,
                                    'setuid_files': setuid_files})
        chmod = which('chmod')
        chmod('555', script)

    # Until tty output works better from build steps, this ends up in
    # the build log.  See https://github.com/spack/spack/pull/10412.
    @run_after('install')
    def caveats(self):
        tty.warn("""
        For full functionality, you'll need to chown and chmod some files
        after installing the package.  This has security implications.
        See: https://singularity.lbl.gov/docs-security for details.

        We've installed a script that will make the necessary changes;
        read through it and then execute it as root (e.g. via sudo).

        The script is named:

        {0}
        """.format(self.perm_script_path()))
