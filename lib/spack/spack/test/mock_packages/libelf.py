from spack import *

class Libelf(Package):
    homepage = "http://www.mr511.de/software/english.html"
    url      = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

    versions =   {'0.8.13' : '4136d7b4c04df68b686570afa26988ac',
                  '0.8.12' : 'e21f8273d9f5f6d43a59878dc274fec7',
                  '0.8.10' : '9db4d36c283d9790d8fa7df1f4d7b4d9' }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--enable-shared",
                  "--disable-dependency-tracking",
                  "--disable-debug")
        make()

        # The mkdir commands in libelf's intsall can fail in parallel
        make("install", parallel=False)
