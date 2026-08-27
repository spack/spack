# Windows PE/COFF test fixtures

Binaries used by `lib/spack/spack/test/relocate_windows.py` to exercise the ctypes-level
PE inspection in `spack.relocate` against real files. They are deliberately tiny: each is
compiled with `/NODEFAULTLIB` and a custom entry point so no CRT is linked in, keeping
every fixture between 0.8 KB and 3.6 KB. They are only ever inspected, never executed.

| File | Built with | What it is for |
| --- | --- | --- |
| `calc.dll` | MSVC compiler wrapper | DLL carrying the `spack`/`SPACKRESOURCE` resource |
| `calc.lib` | MSVC compiler wrapper | Import library whose name field is the padded absolute path to `calc.dll` |
| `tester.exe` | MSVC compiler wrapper | EXE importing `calc.dll`, with its own resource and no exports |
| `plain.dll` | stock `link.exe` | Negative case: a DLL with no spack resource |
| `static.lib` | stock `lib.exe` | Negative case: a true static archive, not an import library |
| `sfn_calc.dll` | MSVC compiler wrapper | Linked from a path over the wrapper's 143-character limit, so its resource holds an 8.3 short path |
| `sfn_calc.lib` | MSVC compiler wrapper | Import library for `sfn_calc.dll` |

`fixtures.txt` records the absolute path each PE was linked at — what the wrapper
stores (padded) in the resource and in the import library name field. The fixtures
are staged under a fixed `C:\spack-pe-fixtures` rather than `%TEMP%`, so that path
is the same for anyone who regenerates them instead of recording whoever ran the
script last. Set `SPACK_PE_FIXTURE_STAGE` to stage elsewhere, but note that changes
the recorded paths, so commit the regenerated `fixtures.txt` with the binaries.

The tests read the paths from `fixtures.txt` rather than hard coding them, because
the `sfn_calc.dll` entry still depends on how 8.3 names came out on the generating
machine.

## Regenerating

From a Visual Studio Developer Command Prompt:

```
generate_fixtures.bat [path-to-msvc-wrapper-repo]
```

The wrapper lives in its own repository, so its path is required: pass it as the
first argument or set `SPACK_MSVC_WRAPPER_ROOT`. It must already have a built
`install\cl.exe` (`nmake cl.exe`). The script rewrites every binary here plus
`fixtures.txt`; commit all of them together.

The `sfn_calc.*` pair additionally requires 8.3 short filename creation to be enabled on
the staging volume. If it is not, the script says so and skips those two files, and the
tests that need them skip in turn. Enable it with `fsutil 8dot3name set 0` from an
elevated prompt.

Sources live in `src/`.
