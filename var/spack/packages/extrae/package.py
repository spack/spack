from spack import *

# typical working line with extrae 3.0.1
# ./configure --prefix=/usr/local --with-mpi=/usr/lib64/mpi/gcc/openmpi --with-unwind=/usr/local --with-papi=/usr --with-dwarf=/usr --with-elf=/usr --with-dyninst=/usr --with-binutils=/usr --with-xml-prefix=/usr --enable-openmp --enable-nanos --enable-pthread --disable-parallel-merge LDFLAGS=-pthread

class Extrae(Package):
    """Extrae is the package devoted to generate tracefiles which can
       be analyzed later by Paraver. Extrae is a tool that uses
       different interposition mechanisms to inject probes into the
       target application so as to gather information regarding the
       application performance. The Extrae instrumentation package can
       instrument the MPI programin model, and the following parallel
       programming models either alone or in conjunction with MPI :
       OpenMP, CUDA, OpenCL, pthread, OmpSs"""
    homepage = "http://www.bsc.es/computer-sciences/extrae"
    url      = "http://www.bsc.es/ssl/apps/performanceTools/files/extrae-3.0.1.tar.bz2"
    version('3.0.1', 'a6a8ca96cd877723cd8cc5df6bdb922b')

    depends_on("mpi")
    depends_on("dyninst")
    depends_on("libunwind")
    depends_on("boost")
    depends_on("libdwarf")
    depends_on("papi")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich2' in spec:
            mpi = spec['mvapich2']

        configure("--prefix=%s"				% prefix,
	            "--with-mpi=%s"				% mpi.prefix,
	            "--with-unwind=%s"			% spec['libunwind'].prefix,
	            "--with-dyninst=%s"			% spec['dyninst'].prefix,
	            "--with-boost=%s"			% spec['boost'].prefix,
	            "--with-dwarf=%s"			% spec['libdwarf'].prefix,
	            "--with-papi=%s"			% spec['papi'].prefix,
	            "--with-dyninst-headers=%s"	% spec['dyninst'].prefix.include,
	            "--with-dyninst-libs=%s"	% spec['dyninst'].prefix.lib)

        make()
        make("install", parallel=False)

