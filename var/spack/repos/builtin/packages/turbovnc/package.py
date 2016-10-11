from spack import *

class Turbovnc(Package):
    """TurboVNC is a derivative of VNC (Virtual Network Computing) 
 that is tuned to provide peak performance for 3D and video workloads.
 TurboVNC was originally a fork of TightVNC 1.3.x, 
 on the surface, the X server and Windows viewer still behave similarly to their parents."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.turbovnc.org/"
    url      = "http://downloads.sourceforge.net/project/turbovnc/2.0.1/turbovnc-2.0.1.tar.gz"

    version('2.0.1', 'a279fdb9ac86a1ebe82f85ab68353dcc',
            url      = "http://downloads.sourceforge.net/project/turbovnc/2.0.1/turbovnc-2.0.1.tar.gz"
    )
    version('2.0.91', '1e203cc533103cf7bd1186c7fd620186',
            url      = "http://downloads.sourceforge.net/project/turbovnc/2.0.91%20%282.1beta2%29/turbovnc-2.0.91.tar.gz"
            
    )

    # FIXME: Add dependencies if this package requires them.
    variant('java', default=False, description='Enable Java build')

   
    depends_on('cmake', type='build')
    depends_on("libjpeg-turbo")
    depends_on("openssl")

    def install(self, spec, prefix):
        def feature_to_bool(feature, on='ON', off='OFF'):
            if feature in spec:
                return on
            return off
#        layout = YamlDirectoryLayout(self.tmpdir)
#        rel_path=layout.relative_path_for_spec(spec)
        feature_args = []
        # FIXME: Modify the configure line to suit your build system here.
        if not '+java' in spec:
            feature_args.append('-DTVNC_BUILDJAVA=%s' % feature_to_bool('+java'))
            feature_args.append('-DTVNC_BUILDNATIVE=%s' % feature_to_bool('+java'))
        feature_args.append('-DCMAKE_VERBOSE_MAKEFILE=ON')
        feature_args.extend(std_cmake_args)
        print ("------------feature_args-->" , feature_args)
        cmake('.', *feature_args)

        # FIXME: Add logic to build and install here
        make()
        make("install")
