from spack import *

class Ghostscript(Package):
    """an interpreter for the PostScript language and for PDF. """
    homepage = "http://ghostscript.com/"
    url      = "https://github.com/ArtifexSoftware/ghostpdl-downloads/archive/gs918.tar.gz"

    version('918', '0d6b529eee942ec80422e91d6fb833e6')

    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

