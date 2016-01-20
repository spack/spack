from spack import *
import os


class Mumps(Package):
    """MUMPS: a MUltifrontal Massively Parallel sparse direct Solver"""

    homepage = "http://mumps.enseeiht.fr"
    url      = "http://mumps.enseeiht.fr/MUMPS_5.0.1.tar.gz"

    version('5.0.1', 'b477573fdcc87babe861f62316833db0')

    variant('mpi', default=True, description='Activate the compilation of MUMPS with the MPI support')
    variant('scotch', default=False, description='Activate Scotch as a possible ordering library')
    variant('ptscotch', default=False, description='Activate PT-Scotch as a possible ordering library')
    variant('metis', default=False, description='Activate Metis as a possible ordering library')
    variant('parmetis', default=False, description='Activate Parmetis as a possible ordering library')
    variant('double', default=True, description='Activate dmumps')
    variant('float', default=True, description='Activate smumps')
    variant('complex', default=True, description='Activate cmumps and/or zmumps')
    variant('idx64', default=False, description='Use int64_t/integer*8 as default index type')
    variant('double', default=False, description='Use double precision floating point types')

    
    depends_on('scotch + esmumps', when='~ptscotch+scotch')
    depends_on('scotch + esmumps + mpi', when='+ptscotch')
    depends_on('metis', when='~parmetis+metis')
    depends_on('parmetis', when="+parmetis")
    depends_on('blas')
    depends_on('scalapack', when='+mpi')
    depends_on('mpi', when='+mpi')
    
    def patch(self):
        if ('+parmetis' in self.spec or '+ptscotch' in self.spec) and '+mpi' not in self.spec:
            raise RuntimeError('You cannot use the variants parmetis or ptscotch without mpi')
        
        makefile_conf = ["LIBBLAS = -L%s -lblas" % self.spec['blas'].prefix.lib]

        orderings = ['-Dpord']
        
        if '+ptscotch' in self.spec or '+scotch' in self.spec:
            join_lib = ' -l%s' % ('pt' if '+ptscotch' in self.spec else '')
            makefile_conf.extend(
                ["ISCOTCH = -I%s" % self.spec['scotch'].prefix.include,
                 "LSCOTCH = -L%s %s%s" % (self.spec['scotch'].prefix.lib,
                                          join_lib,
                                          join_lib.join(['esmumps', 'scotch', 'scotcherr']))])
            orderings.append('-Dscotch')
            if '+ptscotch' in self.spec:
                orderings.append('-Dptscotch')

        if '+parmetis' in self.spec or '+metis' in self.spec:
            libname = 'parmetis' if '+parmetis' in self.spec else 'metis'
            makefile_conf.extend(
                ["IMETIS = -I%s" % self.spec[libname].prefix.include,
                 "LMETIS = -L%s -l%s" % (self.spec[libname].prefix.lib, libname)])

            orderings.append('-Dmetis')
            if '+parmetis' in self.spec:
                orderings.append('-Dparmetis')

        makefile_conf.append("ORDERINGSF = %s" % (' '.join(orderings)))

        if '+idx64' in self.spec:
            makefile_conf.extend(
                ['OPTF    = -O  -DALLOW_NON_INIT %s' % '-fdefault-integer-8' if self.compiler.name == "gcc" else '-i8',
                 'OPTL    = -O ',
                 'OPTC    = -O -DINTSIZE64'])
        else:
            makefile_conf.extend(
                ['OPTF    = -O  -DALLOW_NON_INIT',
                 'OPTL    = -O ',
                 'OPTC    = -O '])


        if '+mpi' in self.spec:
            makefile_conf.extend(
                ["CC = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpicc'),
                 "FC = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
                 "FL = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
                 "SCALAP = %s" % self.spec['scalapack'].fc_link])
        else:
            makefile_conf.extend(
                ["CC = cc",
                 "FC = fc",
                 "FL = fc",
                 "MUMPS_TYPE = seq"])

        makefile_inc_template = join_path(os.path.dirname(self.module.__file__),
                                          'Makefile.inc')
        with open(makefile_inc_template, "r") as fh:
            makefile_conf.extend(fh.read().split('\n'))
        
        with working_dir('.'):
            with open("Makefile.inc", "w") as fh:
                makefile_inc = '\n'.join(makefile_conf)
                fh.write(makefile_inc)



    def install(self, spec, prefix):
        make_libs = []

        # the coice to compile ?examples is to have kind of a sanity
        # check on the libraries generated.
        if '+float' in spec:
            make_libs.append('sexamples')
            if '+complex' in spec:
                make_libs.append('cexamples')

        if '+double' in spec:
            make_libs.append('dexamples')
            if '+complex' in spec:
                make_libs.append('zexamples')

        make(*make_libs)

        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        if '~mpi' in spec:
            install('libseq/libmpiseq.a', prefix.lib)
