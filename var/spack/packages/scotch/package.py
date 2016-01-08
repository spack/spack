from spack import *
import glob
import os

class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""
    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    url      = "http://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc')

    depends_on('mpi')


    def patch(self):
        with working_dir('src/Make.inc'):
            makefiles = glob.glob('Makefile.inc.x86-64_pc_linux2*')
            filter_file(r'^CCS\s*=.*$', 'CCS = cc', *makefiles)
            filter_file(r'^CCD\s*=.*$', 'CCD = cc', *makefiles)


    def install(self, spec, prefix):
        # Currently support gcc and icc on x86_64 (maybe others with
        # vanilla makefile)
        makefile = 'Make.inc/Makefile.inc.x86-64_pc_linux2'
        if spec.satisfies('%icc'):
            makefile += '.icc'

        with working_dir('src'):
            force_symlink(makefile, 'Makefile.inc')
            for app in ('scotch', 'ptscotch'):
                make(app)

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share_man1)

