from spack import *
import shutil

class Objconv(Package):
    """Object file converter"""
    homepage = "http://www.agner.org/optimize/"
    url      = "http://www.agner.org/optimize/objconv.zip"

    version('2015-12-09', 'fcf8f01a5683387e17df6d21497d53fa')

    def install(self, spec, prefix):
        # unzip stalls if the unpacked files already exist
        shutil.rmtree('spack-build', ignore_errors=True)
        with working_dir('spack-build', create=True):
            # The downloaded archive contains another archive
            unzip = which('unzip')
            unzip('../source.zip')
            # Create a makefile
            with open('Makefile', 'w') as f:
                f.write("""
CXX = c++ -g -O2
SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:%.cpp=%.o)
objconv: $(OBJS); $(CXX) -o $@ $^
%.o: %.cpp; $(CXX) -c $*.cpp
""")
            make()
            mkdirp(prefix.bin)
            install('objconv', '%s/objconv' % prefix.bin)
