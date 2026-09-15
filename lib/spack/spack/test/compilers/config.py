# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

import pytest

import spack.caches
import spack.compilers.config
import spack.compilers.libraries
import spack.config
import spack.repo
import spack.spec
from spack.test.utilities import UnusableGlobal


@pytest.mark.skipif(sys.platform == "win32", reason="Cannot execute bash script on Windows")
def test_compilers_config_reads_no_global(
    mutable_config, mock_packages, mock_executable, monkeypatch
):
    """Tests that the functions in spack.compilers.config read the configuration and the compiler
    cache only from their arguments.
    """
    gcc_path = mock_executable(
        "gcc",
        output="""\
for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '4.5.3'
    fi
done
""",
    )
    prefix = gcc_path.parent.parent
    arch = spack.spec.ArchSpec.default_arch()
    # The repository indexes are built lazily through a cache created from spack.config.CONFIG
    mock_packages.packages_with_tags("compiler")

    with monkeypatch.context() as m:
        for module, attribute in [
            (spack.config, "CONFIG"),
            (spack.caches, "MISC_CACHE"),
            (spack.compilers.libraries, "COMPILER_CACHE"),
        ]:
            m.setattr(module, attribute, UnusableGlobal(f"{module.__name__}.{attribute}"))

        # spack.repo.PATH is broken only for detection: CompilerRemover reads it in satisfies
        with monkeypatch.context() as detection:
            detection.setattr(spack.repo, "PATH", UnusableGlobal("spack.repo.PATH"))

            new_compilers = spack.compilers.config.find_compilers(
                [str(prefix)],
                configuration=mutable_config,
                repo=mock_packages,
                scope="site",
                max_workers=1,
            )
            assert [x.format("{name}@{version}") for x in new_compilers] == ["gcc@4.5.3"]

        all_compilers = spack.compilers.config.all_compilers(
            mutable_config, repo=mock_packages, init_config=False
        )
        gcc = [x for x in all_compilers if x.satisfies("gcc@=4.5.3")]
        assert len(gcc) == 1
        assert gcc[0].external_path == str(prefix)

        assert gcc[0] in spack.compilers.config.compilers_for_arch(
            arch, configuration=mutable_config, repo=mock_packages
        )
        assert not spack.compilers.config.select_new_compilers(
            gcc, configuration=mutable_config, repo=mock_packages
        )
        assert mutable_config.get_config_filename(
            "site", "packages"
        ) in spack.compilers.config.compiler_config_files(mutable_config, repo=mock_packages)

        detector = spack.compilers.libraries.CompilerPropertyDetector(
            gcc[0], repo=mock_packages, cache=spack.compilers.libraries.CompilerCache()
        )
        assert detector.implicit_rpaths() == []

        remover = spack.compilers.config.CompilerRemover(mutable_config, repo=mock_packages)
        removed = remover.mark_compilers(match="gcc@4.5.3", scope="site")
        assert [x.format("{name}@{version}") for x in removed] == ["gcc@4.5.3"]
        remover.flush()

        assert not any(
            x.satisfies("gcc@=4.5.3")
            for x in spack.compilers.config.all_compilers(
                mutable_config, repo=mock_packages, init_config=False
            )
        )
