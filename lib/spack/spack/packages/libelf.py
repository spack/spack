from spack import *

class Libelf(Package):
    """libelf lets you read, modify or create ELF object files in an
       architecture-independent way. The library takes care of size
       and endian issues, e.g. you can process a file for SPARC
       processors on an Intel-based system."""

    homepage = "http://www.mr511.de/software/english.html"
    url      = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

    versions = { '0.8.13' : '4136d7b4c04df68b686570afa26988ac',
                 '0.8.12' : 'e21f8273d9f5f6d43a59878dc274fec7', }

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--enable-shared",
                  "--disable-dependency-tracking",
                  "--disable-debug")
        make()

        # The mkdir commands in libelf's install can fail in parallel
        make("install", parallel=False)
