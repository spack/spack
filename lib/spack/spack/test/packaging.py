"""
This test checks the binary packaging infrastructure
"""
import pytest
import spack
import spack.store
from spack.database import Database
from spack.directory_layout import YamlDirectoryLayout
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.spec import Spec
from spack.stage import Stage
from spack.binary_distribution import *
from spack.relocate import *
from llnl.util.filesystem import *
import os 

@pytest.fixture(scope='function')
def mock_gpg_config():
    orig_gpg_keys_path = spack.gpg_keys_path
    spack.gpg_keys_path = spack.mock_gpg_keys_path
    yield
    spack.gpg_keys_path = orig_gpg_keys_path


@pytest.fixture()
def install_mockery(tmpdir, config, builtin_mock):
    """Hooks a fake install directory and a fake db into Spack."""
    layout = spack.store.layout
    db = spack.store.db
    # Use a fake install directory to avoid conflicts bt/w
    # installed pkgs and mock packages.
    spack.store.layout = YamlDirectoryLayout(str(tmpdir))
    spack.store.db = Database(str(tmpdir))
    # We use a fake package, so skip the checksum.
    spack.do_checksum = False
    yield
    # Turn checksumming back on
    spack.do_checksum = True
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.db = db


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher

@pytest.mark.usefixtures('install_mockery', 'mock_gpg_config')
def test_packaging(mock_archive):
    # tweak patchelf to only do a download
    spec = Spec("patchelf")
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(pkg.fetcher, pkg)

    # Install the test package
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    pkg.do_install()

    # Put some non-relocatable file in there
    filename = join_path(spec.prefix, "dummy.txt")
    with open(filename, "w") as script:
        script.write(spec.prefix)

    # Create the build cache  and
    # put it directly into the mirror
    mirrors = {}
    with Stage('spack-mirror-test',keep=True) as stage:
        mirror_root = join_path(stage.path, 'test-mirror')
        os.chdir(stage.path)
        specs=[spec]
        spack.mirror.create(
            mirror_root, specs, no_checksum=True
        )
        build_tarball(spec, mirror_root+'/build_cache/', sign=False)

        # register mirror with spack config
        mirrors['spack-mirror-test'] = 'file://' + mirror_root


        # Validate the relocation information
        buildinfo = read_buildinfo_file(spec)
        assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])

        # Uninstall the package
        pkg.do_uninstall(force=True) 
