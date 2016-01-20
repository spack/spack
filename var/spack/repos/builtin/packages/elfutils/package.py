from spack import *

class Elfutils(Package):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"

    version('0.163',
            git='git://git.fedorahosted.org/git/elfutils.git',
            tag='elfutils-0.163')

    provides('elf')

    def install(self, spec, prefix):
        autoreconf = which('autoreconf')
        autoreconf('-if')

        configure('--prefix=%s' % prefix, '--enable-maintainer-mode')
        make()
        make("install")

