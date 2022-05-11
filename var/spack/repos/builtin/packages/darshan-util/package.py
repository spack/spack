# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class DarshanUtil(AutotoolsPackage):
    """Darshan (util) is collection of tools for parsing and summarizing log
    files produced by Darshan (runtime) instrumentation. This package is
    typically installed on systems (front-end) where you intend to analyze
    log files produced by Darshan (runtime)."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan/"
    url      = "https://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"
    git      = "https://github.com/darshan-hpc/darshan.git"

    maintainers = ['shanedsnyder', 'carns']

    tags = ['e4s']

    version('main', branch='main', submodules='True')
    version('3.3.1', sha256='281d871335977d0592a49d053df93d68ce1840f6fdec27fea7a59586a84395f7')
    version('3.3.0', sha256='2e8bccf28acfa9f9394f2084ec18122c66e45d966087fa2e533928e824fcb57a')
    version('3.3.0-pre2', sha256='0fc09f86f935132b7b05df981b05cdb3796a1ea02c7acd1905323691df65e761')
    version('3.3.0-pre1', sha256='1c655359455b5122921091bab9961491be58a5f0158f073d09fe8cc772bd0812')
    version('3.2.1', sha256='d63048b7a3d1c4de939875943e3e7a2468a9034fcb68585edbc87f57f622e7f7')
    version('3.2.0', sha256='4035435bdc0fa2a678247fbf8d5a31dfeb3a133baf06577786b1fe8d00a31b7e')
    version('3.1.8', sha256='3ed51c8d5d93b4a8cbb7d53d13052140a9dffe0bc1a3e1ebfc44a36a184b5c82')
    version('3.1.7', sha256='9ba535df292727ac1e8025bdf2dc42942715205cad8319d925723fd88709e8d6')
    version('3.1.6', sha256='21cb24e2a971c45e04476e00441b7fbea63d2afa727a5cf8b7a4a9d9004dd856')
    version('3.1.0', sha256='b847047c76759054577823fbe21075cfabb478cdafad341d480274fb1cef861c')
    version('3.0.0', sha256='95232710f5631bbf665964c0650df729c48104494e887442596128d189da43e0')

    variant('bzip2', default=False, description="Enable bzip2 compression")
    variant('apmpi', default=False, description='Compile with AutoPerf MPI module support')
    variant('apxc', default=False, description='Compile with AutoPerf XC module support')

    depends_on('zlib')
    depends_on('bzip2', when="+bzip2", type=("build", "link", "run"))
    depends_on('autoconf', type='build', when='@main')
    depends_on('automake', type='build', when='@main')
    depends_on('libtool',  type='build', when='@main')
    depends_on('m4',       type='build', when='@main')

    patch('retvoid.patch', when='@3.2.0:3.2.1')

    conflicts('+apmpi', when='@:3.2.1',
              msg='+apmpi variant only available starting from version 3.3.0')
    conflicts('+apxc', when='@:3.2.1',
              msg='+apxc variant only available starting from version 3.3.0')

    @property
    def configure_directory(self):
        return 'darshan-util'

    def configure_args(self):
        spec = self.spec
        extra_args = []

        extra_args.append('CC=%s' % self.compiler.cc)
        extra_args.append('--with-zlib=%s' % spec['zlib'].prefix)
        if '+apmpi' in spec:
            if self.version < Version('3.3.2'):
                extra_args.append('--enable-autoperf-apmpi')
            else:
                extra_args.append('--enable-apmpi-mod')
        if '+apxc' in spec:
            if self.version < Version('3.3.2'):
                extra_args.append('--enable-autoperf-apxc')
            else:
                extra_args.append('--enable-apxc-mod')

        return extra_args

    @property
    def basepath(self):
        return join_path('darshan-test', 'example-output')

    @run_after('install')
    def _copy_test_inputs(self):
        # add darshan-test/example-output/mpi-io-test-spack-expected.txt"
        test_inputs = [
            join_path(self.basepath,
                      "mpi-io-test-x86_64-{0}.darshan".format(self.spec.version))]
        self.cache_extra_test_sources(test_inputs)

    def _test_parser(self):
        purpose = "Verify darshan-parser can parse an example log \
                   from the current version and check some expected counter values"
        # Switch to loading the expected strings from the darshan source in future
        # filename = self.test_suite.current_test_cache_dir.
        #            join(join_path(self.basepath, "mpi-io-test-spack-expected.txt"))
        # expected_output = self.get_escaped_text_output(filename)
        expected_output = [r"POSIX\s+-1\s+\w+\s+POSIX_OPENS\s+\d+",
                           r"MPI-IO\s+-1\s+\w+\s+MPIIO_INDEP_OPENS\s+\d+",
                           r"STDIO\s+0\s+\w+\s+STDIO_OPENS\s+\d+"]
        logname = self.test_suite.current_test_cache_dir.join(
            join_path(self.basepath,
                      "mpi-io-test-x86_64-{0}.darshan".format(self.spec.version)))
        exe = 'darshan-parser'
        options = [logname]
        status = [0]
        installed = True
        self.run_test(exe,
                      options,
                      expected_output,
                      status,
                      installed,
                      purpose,
                      skip_missing=False,
                      work_dir=None)

    def test(self):
        self._test_parser()
