# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.build_environment as be
import spack.concretize
import spack.config
from spack.util.environment import EnvironmentModifications


def _collect_mods_by_name(env_mods):
    """Helper: return dict of {var_name: [values]} from env modifications."""
    by_name = {}
    for mod in env_mods.env_modifications:
        name = mod.name
        value = getattr(mod, "value", "")
        by_name.setdefault(name, []).append(value)
    return by_name


def _normalize(values):
    """Normalize path separators to forward slashes for cross-platform compatibility."""
    return [v.replace("\\", "/") for v in values]


@pytest.mark.usefixtures("install_mockery", "mock_fetch")
class TestInjectFfilePrefixMap:
    """Tests for _inject_ffile_prefix_map in build_environment.py."""

    def _get_pkg(self, spec_str="mpileaks"):
        """Concretize and return a mock package for testing."""
        spec = spack.concretize.concretize_one(spec_str)
        assert spec.concrete
        return spec.package

    def test_debug_flag_g_is_injected(self):
        """-g must be present in C, C++, Fortran flag variables."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in (
            "SPACK_CFLAGS",
            "SPACK_CXXFLAGS",
            "SPACK_FFLAGS",
            "SPACK_FCFLAGS",
            "CFLAGS",
            "CXXFLAGS",
            "FFLAGS",
            "FCFLAGS",
        ):
            values = by_name.get(var, [])
            assert any("-g" in v for v in values), f"-g not found in {var}. Got: {values}"

    def test_ffile_prefix_map_src_is_injected(self):
        """-ffile-prefix-map pointing to .spack/src must be present."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in ("SPACK_CFLAGS", "SPACK_CXXFLAGS", "CFLAGS", "CXXFLAGS"):
            values = _normalize(by_name.get(var, []))
            assert any("-ffile-prefix-map" in v and ".spack/src" in v for v in values), (
                f"-ffile-prefix-map with .spack/src not found in {var}. "
                f"Got: {by_name.get(var, [])}"
            )

    def test_permanent_path_contains_prefix(self):
        """The permanent path in -ffile-prefix-map must be under the package prefix."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)
        prefix = str(pkg.spec.prefix).replace("\\", "/")

        all_flag_values = []
        for var in ("SPACK_CFLAGS", "CFLAGS"):
            all_flag_values.extend(_normalize(by_name.get(var, [])))

        prefix_map_flags = [v for v in all_flag_values if "-ffile-prefix-map" in v]

        assert prefix_map_flags, "No -ffile-prefix-map flags found at all"
        assert any(prefix in v for v in prefix_map_flags), (
            f"Package prefix {prefix} not found in any -ffile-prefix-map flag. "
            f"Got: {prefix_map_flags}"
        )

    def test_staging_path_is_not_permanent_destination(self):
        """The staging path must appear only as the OLD side of -ffile-prefix-map,
        never as the NEW (permanent) side."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        try:
            staging_src = pkg.stage.source_path
        except Exception:
            staging_src = str(pkg.stage.path)

        staging_src = staging_src.replace("\\", "/")

        for var in ("SPACK_CFLAGS", "CFLAGS"):
            for v in _normalize(by_name.get(var, [])):
                if "-ffile-prefix-map" in v:
                    # Format is: -ffile-prefix-map=OLD=NEW
                    # Strip the flag name, then split OLD=NEW on first '='
                    remainder = v[len("-ffile-prefix-map=") :]
                    parts = remainder.split("=", 1)
                    if len(parts) == 2:
                        new_path = parts[1]
                        assert staging_src not in new_path, (
                            f"Staging path {staging_src} appears as the permanent "
                            f"(NEW) side of -ffile-prefix-map in {var}: {v}"
                        )

    def test_fortran_flags_also_injected(self):
        """Fortran flag variables must also get -g and -ffile-prefix-map."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in ("SPACK_FFLAGS", "SPACK_FCFLAGS", "FFLAGS", "FCFLAGS"):
            values = _normalize(by_name.get(var, []))
            assert any("-g" in v for v in values), (
                f"-g not found in Fortran variable {var}. Got: {by_name.get(var, [])}"
            )
            assert any("-ffile-prefix-map" in v for v in values), (
                f"-ffile-prefix-map not found in Fortran variable {var}. "
                f"Got: {by_name.get(var, [])}"
            )

    def test_nvcc_hip_flags_use_xcompiler_syntax(self):
        """CUDA/HIP flags must use -Xcompiler= syntax to forward flags to host compiler."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in ("CUDA_FLAGS", "NVCCFLAGS", "HIPFLAGS"):
            values = by_name.get(var, [])
            assert any(v == "-Xcompiler=-g" for v in values), (
                f"-Xcompiler=-g not found in {var}. Got: {values}"
            )
            assert any(v.startswith("-Xcompiler=-ffile-prefix-map=") for v in values), (
                f"-Xcompiler=-ffile-prefix-map=... not found in {var}. Got: {values}"
            )

    def test_flags_not_injected_by_default_without_config(self):
        """Without config:debug_info set, setup_package must NOT inject these flags.
        This tests the gating logic in setup_package, not _inject_ffile_prefix_map directly."""
        assert not spack.config.get("config:debug_info"), (
            "config:debug_info should be False/unset by default"
        )

    def test_flags_injected_when_config_enabled(self):
        """With config:debug_info: true, the flags must appear in the build environment."""
        pkg = self._get_pkg()
        env = EnvironmentModifications()

        with spack.config.override("config:debug_info", True):
            assert spack.config.get("config:debug_info"), (
                "config:debug_info should be True after override"
            )
            be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        assert any(
            "-g" in v for var in ("SPACK_CFLAGS", "CFLAGS") for v in by_name.get(var, [])
        ), "-g not found after config:debug_info override"

        assert any(
            "-ffile-prefix-map" in v
            for var in ("SPACK_CFLAGS", "CFLAGS")
            for v in by_name.get(var, [])
        ), "-ffile-prefix-map not found after config:debug_info override"

    def test_build_dir_remap_injected_for_cmake_package(self):
        """For CMake packages with a separate build_directory, .spack/build must be remapped."""
        # cmake-client or similar mock CMake package that has build_directory set
        pkg = self._get_pkg("cmake-client")
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in ("SPACK_CFLAGS", "CFLAGS"):
            values = _normalize(by_name.get(var, []))
            assert any("-ffile-prefix-map" in v and ".spack/build" in v for v in values), (
                f"-ffile-prefix-map with .spack/build not found in {var}. "
                f"Got: {by_name.get(var, [])}"
            )

    def test_build_dir_remap_absent_for_non_cmake_package(self):
        """For packages without a separate build_directory, .spack/build must NOT appear."""
        pkg = self._get_pkg("mpileaks")  # Autotools, no separate build_directory
        env = EnvironmentModifications()

        be._inject_ffile_prefix_map(pkg, env)

        by_name = _collect_mods_by_name(env)

        for var in ("SPACK_CFLAGS", "CFLAGS"):
            values = _normalize(by_name.get(var, []))
            assert not any("-ffile-prefix-map" in v and ".spack/build" in v for v in values), (
                f"Unexpected .spack/build remap found in {var} for non-CMake pkg. "
                f"Got: {by_name.get(var, [])}"
            )
