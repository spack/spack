from spack import *

class OsuMicroBenchmarks(Package):
    """The Ohio MicroBenchmark suite is a collection of independent MPI
    message passing performance microbenchmarks developed and written at
    The Ohio State University. It includes traditional benchmarks and
    performance measures such as latency, bandwidth and host overhead
    and can be used for both traditional and GPU-enhanced nodes."""

    homepage = "http://mvapich.cse.ohio-state.edu/benchmarks/"
    url      = "http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.3.tar.gz"

    version('5.3', '42e22b931d451e8bec31a7424e4adfc2')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('mpi')
    depends_on('cuda', when='+cuda')


    def install(self, spec, prefix):
        config_args = [
            'CC=%s'  % spec['mpi'].prefix.bin + '/mpicc',
            'CXX=%s' % spec['mpi'].prefix.bin + '/mpicxx',
            'LDFLAGS=-lrt',
            '--prefix=%s' % prefix
        ]

        if '+cuda' in spec:
            config_args.extend([
                '--enable-cuda',
                '--with-cuda=%s' % spec['cuda'].prefix,
            ])

        configure(*config_args)

        make()
        make('install')
