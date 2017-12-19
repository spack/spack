##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

# Based on package.py for picard
class Pilon(Package):
    """Pilon is an automated genome assembly improvement and variant detection
       tool."""

    homepage = "https://github.com/broadinstitute/pilon"
    url      = "https://github.com/broadinstitute/pilon/releases/download/v1.22/pilon-1.22.jar"
    
    version('1.22', '3c45568dc1b878a9a0316410ec62ab04', expand=False)

    depends_on('java@7', type='run')
    
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        # The list of files to install varies with release...
        # ... but skip the spack-{build.env}.out files.
        files = [x for x in glob.glob("*") if not re.match("^spack-", x)]
        for f in files:
            install(f, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "pilon.sh")
        script = join_path(prefix.bin, "pilon")
        copyfile(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('pilon.jar', join_path(prefix.bin, 'pilon.jar'),
                    script, **kwargs)

#    def setup_environment(self, spack_env, run_env):
#        """The Picard docs suggest setting this as a convenience."""
#        run_env.prepend_path('PICARD',
#                             join_path(self.prefix, 'bin', 'picard.jar'))
#
#    def url_for_version(self, version):
#        if version < Version('2.6.0'):
#            return self._oldurlfmt.format(version)
#        else:
#            return self._urlfmt.format(version)
                                        
