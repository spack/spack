from spack import *
import os

class Astyle(Package):
    """A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI, Objective-C, C#, and Java Source Code."""
    homepage = "http://astyle.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/astyle/astyle/astyle%202.04/astyle_2.04_linux.tar.gz"

    version('2.04', '30b1193a758b0909d06e7ee8dd9627f6')

    def install(self, spec, prefix):

        with working_dir('src'):
            make('-f',
                join_path(self.stage.source_path,'build','clang','Makefile'),
                parallel=False)
            mkdirp(self.prefix.bin)
            install(join_path(self.stage.source_path, 'src','bin','astyle'), self.prefix.bin)
