from spack import *


class EnvironmentModules(Package):
    """Environment Modules for HPC"""

    homepage = "https://sourceforge.net/p/modules/wiki/Home/"
    url      = "http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz"

    version('3.2.10', '8b097fdcb90c514d7540bb55a3cb90fb')

    # Dependencies:
    depends_on('tcl')

    def install(self, spec, prefix):
        # See: https://sourceforge.net/p/modules/bugs/62/
        CPPFLAGS = ['-DUSE_INTERP_ERRORLINE']
        config_args = [
            "--prefix=%s" % prefix,
            "--with-tcl=%s" % join_path(spec['tcl'].prefix, 'lib'),    # It looks for tclConfig.sh
            'CPPFLAGS=%s' % ' '.join(CPPFLAGS)
        ]


        configure(*config_args)
        make()
        make("install")
