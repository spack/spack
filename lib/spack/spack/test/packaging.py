"""
This test checks the binary packaging infrastructure
"""

import spack
from spack.binary_distribution import build_tarball, read_buildinfo_file
from llnl.util.filesystem import *
from spack.directory_layout import YamlDirectoryLayout
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.test.mock_packages_test import *
from spack.test.mock_repo import MockArchive


class PackagingTest(MockPackagesTest):
    """"Installs, packages, deletes, and installs a package"""

    def setUp(self):
        super(PackagingTest, self).setUp()

        # create a simple installable package directory and tarball
        self.repo = MockArchive()

        # We use a fake package, so skip the checksum.
        spack.do_checksum = False
        self.tmpdir = tempfile.mkdtemp()
        self.orig_layout = spack.store.layout
        spack.store.layout = YamlDirectoryLayout(self.tmpdir)

    def tearDown(self):
        super(PackagingTest, self).tearDown()
        self.repo.destroy()

        # Turn checksumming back on
        spack.do_checksum = True

        # restore spack's layout.
        spack.store.layout = self.orig_layout
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def set_up_mirror(self):
        self.mirror_root = join_path(self.tmpdir, "binary-mirror")
        mkdirp(self.mirror_root)
        # register mirror with spack config
        mirrors = {'spack-mirror-test': 'file://' + self.mirror_root}
        spack.config.update_config('mirrors', mirrors)

    def fake_fetchify(self, pkg):
        """Fake the URL for a package so it downloads from a file."""
        fetcher = FetchStrategyComposite()
        fetcher.append(URLFetchStrategy(self.repo.url))
        pkg.fetcher = fetcher

    def test_packaging(self):
        # tweak patchelf to only do a download
        spec = Spec("patchelf")
        spec.concretize()
        pkg = spack.repo.get(spec)
        self.fake_fetchify(pkg)

        # Install the test package
        spec = Spec("trivial_install_test_package").concretized()
        pkg = spack.repo.get(spec)
        self.fake_fetchify(pkg)

        # Put some non-relocatable file in there
        filename = join_path(spec.prefix, "dummy.txt")
        with open(filename, "w") as script:
            script.write(spec.prefix)

        # Create the tarball and
        # put it directly into the mirror
        self.set_up_mirror()
        build_tarball(spec, self.mirror_root)

        # Uninstall the package
        pkg.do_uninstall(force=True)

        # Validate the relocation information
        buildinfo = read_buildinfo_file(spec)
        assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])
