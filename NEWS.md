## Spack v1.0.0
Deprecated the implicit attributes:
- `PackageBase.legacy_buildsystem`
- `Builder.legacy_methods`
- `Builder.legacy_attributes`
- `Builder.legacy_long_methods`

## Package API v2.2
Added to `spack.package`:
- `BuilderWithDefaults`
- `ClassProperty`
- `CompilerPropertyDetector`
- `GenericBuilder`
- `HKEY`
- `LC_ID_DYLIB`
- `LinkTree`
- `MachO`
- `ModuleChangePropagator`
- `Package`
- `WindowsRegistryView`
- `apply_macos_rpath_fixups`
- `classproperty`
- `compare_output_file`
- `compare_output`
- `compile_c_and_execute`
- `compiler_spec`
- `create_builder`
- `dedupe`
- `delete_needed_from_elf`
- `delete_rpath`
- `environment_modifications_for_specs`
- `execute_install_time_tests`
- `filter_shebang`
- `filter_system_paths`
- `find_all_libraries`
- `find_compilers`
- `get_cmake_prefix_path`
- `get_effective_jobs`
- `get_elf_compat`
- `get_path_args_from_module_line`
- `get_user`
- `has_shebang`
- `host_platform`
- `is_system_path`
- `join_url`
- `kernel_version`
- `libc_from_dynamic_linker`
- `macos_version`
- `make_package_test_rpath`
- `memoized`
- `microarchitecture_flags_from_target`
- `microarchitecture_flags`
- `module_command`
- `parse_dynamic_linker`
- `parse_elf`
- `path_contains_subdirectory`
- `readlink`
- `safe_remove`
- `sbang_install_path`
- `sbang_shebang_line`
- `set_env`
- `shared_library_suffix`
- `spack_script`
- `static_library_suffix`
- `substitute_version_in_url`
- `windows_sfn`

## Package API v2.1
Added to `spack.package`:
- `CompilerError`
- `SpackError`
